use std::{collections::HashMap, fs::File, net::SocketAddr, sync::Arc};

use animal_classification_core::{AnimalClass, AnimalDescription};
use anyhow::Context;
use axum::{http::StatusCode, routing::post, Json, Router};
use ndarray::{Array2, CowArray};
use ort::{Environment, GraphOptimizationLevel, LoggingLevel, Session, SessionBuilder, Value};

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let state = Arc::new((
        load_session("animal-classes.onnx")?,
        load_classes("input/class.csv")?,
    ));

    let app = Router::new().route(
        "/classify",
        post(move |Json(description)| {
            let state = state.clone();
            async move {
                classify_animal(&(*state).0, &(*state).1, description)
                    .map(|class| Json(class.json()))
                    .map_err(|err| {
                        (
                            StatusCode::INTERNAL_SERVER_ERROR,
                            format!("Something went wrong: {}", err),
                        )
                    })
            }
        }),
    );

    axum::Server::bind(&SocketAddr::new("0.0.0.0".parse().unwrap(), 5000))
        .serve(app.into_make_service())
        .await
        .unwrap();

    Ok(())
}

fn load_session(model_path: &str) -> anyhow::Result<Session> {
    let environment = Environment::builder()
        .with_log_level(LoggingLevel::Verbose)
        .build()?
        .into_arc();
    let session = SessionBuilder::new(&environment)?
        .with_optimization_level(GraphOptimizationLevel::Level1)?
        .with_intra_threads(1)?
        .with_model_from_file(model_path)?;

    Ok(session)
}

fn classify_animal(
    session: &Session,
    classes: &HashMap<i64, AnimalClass>,
    description: AnimalDescription,
) -> anyhow::Result<AnimalClass> {
    let description_array = CowArray::from(to_array(description).into_dyn());
    let input = vec![Value::from_array(session.allocator(), &description_array)?];
    let prediction = session.run(input)?;
    let predicted_animal_class_id = prediction[0]
        .try_extract::<i64>()?
        .view()
        .to_slice()
        .unwrap()[0];
    let class = classes
        .get(&predicted_animal_class_id)
        .context("class not found")?;

    Ok(class.clone())
}

fn load_classes(path: &str) -> anyhow::Result<HashMap<i64, AnimalClass>> {
    let mut classes = HashMap::new();
    let file = File::open(path)?;
    let mut reader = csv::Reader::from_reader(file);
    for result in reader.records() {
        let record = result?;
        let class_id = str::parse(record.get(0).context("missing class number")?)?;
        classes.insert(
            class_id as i64,
            AnimalClass {
                class_id,
                name: record.get(2).context("missing class type")?.into(),
            },
        );
    }
    Ok(classes)
}

fn to_array(desc: AnimalDescription) -> Array2<i64> {
    Array2::from_shape_vec(
        [1, 16],
        vec![
            desc.hair.into(),
            desc.feathers.into(),
            desc.eggs.into(),
            desc.milk.into(),
            desc.airborne.into(),
            desc.aquatic.into(),
            desc.predator.into(),
            desc.toothed.into(),
            desc.backbone.into(),
            desc.breathes.into(),
            desc.venomous.into(),
            desc.fins.into(),
            desc.legs.into(),
            desc.tail.into(),
            desc.domestic.into(),
            desc.catsize.into(),
        ],
    )
    .unwrap()
}

#[test]
fn load_and_classify() -> anyhow::Result<()> {
    tracing_subscriber::fmt::init();

    let session = load_session("../../animal-classes.onnx")?;
    let classes = load_classes("../../input/class.csv")?;

    let aardvark = AnimalDescription {
        hair: 1,
        feathers: 0,
        eggs: 0,
        milk: 1,
        airborne: 0,
        aquatic: 0,
        predator: 1,
        toothed: 1,
        backbone: 1,
        breathes: 1,
        venomous: 0,
        fins: 0,
        legs: 4,
        tail: 0,
        domestic: 0,
        catsize: 1,
    };
    let frog = AnimalDescription {
        hair: 0,
        feathers: 0,
        eggs: 1,
        milk: 0,
        airborne: 0,
        aquatic: 1,
        predator: 1,
        toothed: 1,
        backbone: 1,
        breathes: 1,
        venomous: 1,
        fins: 0,
        legs: 4,
        tail: 0,
        domestic: 0,
        catsize: 0,
    };

    let frog_class = classify_animal(&session, &classes, frog)?;
    let aardvark_class = classify_animal(&session, &classes, aardvark)?;

    assert_eq!(aardvark_class.name, "Mammal");
    assert_eq!(frog_class.name, "Amphibian");

    Ok(())
}
