let fullName = "Indera Ihsan";
let age = 27;
let firstJob = "Data Scientist";
let dreamJob = "Back End Engineer";

console.log(
  "Hi, my name is ",
  fullName,
  "aged ",
  age,
  "i was a ",
  firstJob,
  " and now i am pursuing a career in ",
  dreamJob
);

// this is gonna be the exercise.

let country = "Indonesia";
let continent = "Asia/South East Asia";
let population = 250;

console.log(
  "I am from ",
  country,
  " ",
  continent,
  "which is a large country with ",
  population,
  "millions population"
);

// task boolean learning

const isOldEnough = age >= 18;
console.log(isOldEnough);

if (isOldEnough) {
  console.log(fullName, " is eligible to have a driving license");
}

//typeconversion

let someNumber = "2019";
console.log(someNumber + 2018);
console.log(Number(someNumber) + 2018);

//boolean checking (example if we have a data from a backend)

let someResponse = 250;

if (someResponse) {
  console.log("freya");
} else {
  console.log("someResponse is undefined");
}

//boolean operations

let ableToWritePython = false;
let understandStatistics = true;

let goodCandidate = ableToWritePython && understandStatistics;

if (goodCandidate) {
  console.log(`${fullName} is a good Data scientist`);
}

if (!ableToWritePython) {
  console.log(`${fullName} should learn about python`);
}

if (!understandStatistics) {
  console.log(`${fullName} should learn about statistic`);
}

//ternary operator

const myAge = 30;

myAge >= 18
  ? console.log(" Oh boy i am an adult")
  : console.log("oh dear i am still a kid");
