use ndarray::{Array1, Array2, CowArray};
use ort::{Environment, GraphOptimizationLevel, LoggingLevel, SessionBuilder, Value};

fn main() -> anyhow::Result<()> {
    tracing_subscriber::fmt::init();
    let environment = Environment::builder()
        .with_name("test")
        .with_log_level(LoggingLevel::Verbose)
        .build()?
        .into_arc();
    let mut session = SessionBuilder::new(&environment)?
        .with_optimization_level(GraphOptimizationLevel::Level1)?
        .with_intra_threads(1)?
        .with_model_from_file("../animal-classes.onnx")?;

    let input_name = session.inputs[0].name.clone();
    let label_name = session.outputs[0].name.clone();

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
    let prediction =
        session.run(vec![Value::from_array(
            session.allocator(),
            &CowArray::from(frog.to_array().into_dyn()),
        )?])?[0]
            .try_extract::<i64>()?;

    let animal_class_id = prediction.view().to_slice().unwrap()[0];

    println!("{animal_class_id:?}");

    Ok(())
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
