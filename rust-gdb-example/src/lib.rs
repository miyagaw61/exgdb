#[derive(Clone, Debug)]
pub enum AnimalType {
    Cat,
    Dog,
}

#[derive(Clone, Debug)]
pub struct Animal {
    pub kind: AnimalType,
    pub name: String,
    pub age: usize,
}

#[derive(Clone, Debug)]
pub struct Person {
    pub name: String,
    pub pets: Vec<Animal>,
    pub age: usize,
}
