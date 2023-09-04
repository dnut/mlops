use std::{collections::HashMap, fs::File};

use anyhow::Context;
use ndarray::{Array2, CowArray};
use ort::{Environment, GraphOptimizationLevel, LoggingLevel, Session, SessionBuilder, Value};

fn main() -> anyhow::Result<()> {
    todo!()
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
    let description_as_array = CowArray::from(description.to_array().into_dyn());
    let input = vec![Value::from_array(
        session.allocator(),
        &description_as_array,
    )?];
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
        let id = str::parse(record.get(0).context("missing class number")?)?;
        classes.insert(
            id as i64,
            AnimalClass {
                id,
                name: record.get(2).context("missing class type")?.into(),
            },
        );
    }
    Ok(classes)
}

#[derive(Clone, Copy, Debug)]
pub struct AnimalDescription {
    pub hair: u8,
    pub feathers: u8,
    pub eggs: u8,
    pub milk: u8,
    pub airborne: u8,
    pub aquatic: u8,
    pub predator: u8,
    pub toothed: u8,
    pub backbone: u8,
    pub breathes: u8,
    pub venomous: u8,
    pub fins: u8,
    pub legs: u8,
    pub tail: u8,
    pub domestic: u8,
    pub catsize: u8,
}

impl AnimalDescription {
    fn to_array(self) -> Array2<i64> {
        Array2::from_shape_vec(
            [1, 16],
            vec![
                self.hair.into(),
                self.feathers.into(),
                self.eggs.into(),
                self.milk.into(),
                self.airborne.into(),
                self.aquatic.into(),
                self.predator.into(),
                self.toothed.into(),
                self.backbone.into(),
                self.breathes.into(),
                self.venomous.into(),
                self.fins.into(),
                self.legs.into(),
                self.tail.into(),
                self.domestic.into(),
                self.catsize.into(),
            ],
        )
        .unwrap()
    }
}

#[derive(Clone, Debug)]
pub struct AnimalClass {
    pub id: u8,
    pub name: String,
}

#[test]
fn load_and_classify() -> anyhow::Result<()> {
    tracing_subscriber::fmt::init();

    let session = load_session("../animal-classes.onnx")?;
    let classes = load_classes("../input/class.csv")?;

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
