use serde::{Deserialize, Serialize};
use serde_json::Value;

#[derive(Serialize, Deserialize, Clone, Copy, Debug)]
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

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct AnimalClass {
    pub class_id: u8,
    pub name: String,
}

impl AnimalClass {
    pub fn json(self) -> Value {
        serde_json::json!(self)
    }
}

#[cfg(feature = "http-typed")]
pub mod client {
    use super::*;
    use http_typed::{request_group, Client, HttpMethod, Request, SerdeJson};

    pub type AnimalClassificationClient = Client<AnimalClassification>;

    request_group!(pub AnimalClassification { AnimalDescription });

    impl Request for AnimalDescription {
        type Serializer = SerdeJson;
        type Response = AnimalClass;

        fn method(&self) -> HttpMethod {
            HttpMethod::Post
        }

        fn path(&self) -> String {
            "/classifier".into()
        }
    }
}
