import React, { useState } from 'react';
import { View, Text, TouchableOpacity, TextInput, StyleSheet, Alert } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { ScrollView } from 'react-native';
import { TouchableWithoutFeedback, Keyboard } from 'react-native';




export default function App() {
  const [screen, setScreen] = useState('home');
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [age, setAge] = useState('');
  const [currentQuestions, setCurrentQuestions] = useState([]);
  const [selectedDisease, setSelectedDisease] = useState(null);
  const [textAnswer, setTextAnswer] = useState('');
  const [answers, setAnswers] = useState({});


  const questionsMap = {
    "Thyroid Cancer": [
      { text: 'Do you have enlarged lymph nodes in your neck?', options: ['No', 'Right', 'Extensive', 'Left', 'Bilateral', 'Posterior'] },
      { text: 'What is your tumor classification?', options: ['T1a', 'T1b', 'T2', 'T3a', 'T4a', 'T4b'] },
      { text: 'What is your lymph node classification based on cancer staging?', options: ['N0', 'N1a', 'N1b'] },
      { text: 'How did your cancer respond to treatment?', options: ['Indeterminate', 'Excellent', 'Structural', 'Biochemical Incomplete'] },
    ],
    "Lung\n Cancer": [
      { text: 'How old are you?'},
      { text: 'Do you have peer pressure?', options: ['Yes', 'No'] },
      { text: 'Do you have allergies?', options: ['Yes', 'No'] },
      { text: 'Do you drink alcohol?', options: ['Yes', 'No'] },
    ],
    "Heart Disease": [
      { text: 'What type of chestpain do you experience?', options: ['Typical Angina', 'Atypical Angina', 'Non-Anginal Pain', 'Asymptomatic'] },
      { text: 'What is your maximum heart rate?'},
      { text: 'What is your ST depression induced by exercise relative to rest?'},
      { text: 'What is the number of major vessels colored by flourosopy?', options: ['0', '1', '2', '3'] },
    ],


    "Diabetes": [
      { text: 'What is your BMI?'},
      { text: 'How would you rank your general health (1 is the best, 5 is the worst)', options: ['1', '2', '3', '4', '5'] },
      { text: 'What is your age?'},
      { text: 'Rank your income: \n1 = less than $10k \n5 = less than 35k \n8 = more than 75k', options: ['1', '5', '8'] },
    ]
  };
// Rank you education: n1 = Never attended school or only kindergarten \n2 = Grades 1-8 (Elementary) \n3 = Grades 9-11 (Some high school) \n4 = Grade 12 or GED (High school graduate)  \n5 = College 1-3 years (Some college or technical school)  \n6 = College 4 years+ (College graduate)
 
const handleDiseaseSelection = (disease) => {
  setSelectedDisease(disease);
  setScreen('modeSelection');
  setAnswers({}); // Reset answers
  setPrediction(null); // Reset prediction
  setAge(''); // Clear any input fields
  setTextAnswer(''); // Clear text answer
};


  const handleQuizStart = (mode) => {
    if (mode === 'Normal') {
      setCurrentQuestions(questionsMap[selectedDisease]);
      setScreen('quiz');
      setCurrentQuestion(0);
      setAnswers({}); // Reset answers
      setPrediction(null); // Reset prediction
      setAge(''); // Clear the age input (or any other input field)
      setTextAnswer(''); // Clear the text answer field
    } else if (mode === 'Short') {
      console.log('Short mode selected - Placeholder for future logic');
    }
  };
  


  const handleAnswer = (answer) => {
    const questionText = currentQuestions[currentQuestion].text;
    setAnswers((prevAnswers) => ({
      ...prevAnswers,
      [questionText]: answer,
    }));
  };


  const diseaseMap = {
    "Lung\n Cancer": "lung_cancer",
    "Diabetes": "diabetes",
    "Thyroid Cancer": "thyroid_cancer",
    "Heart Disease": "Heart_Disease"
  };
  /*
  const handleSubmit = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        disease: diseaseMap[selectedDisease], // Correct backend key
        answers: answers, // User responses
      }),
    });


    const data = await response.json();
    Alert.alert("Prediction Result", `You may have: ${data.prediction}`);
  } catch (error) {
    console.error("Error:", error);
    Alert.alert("Error", "Failed to get prediction");
  }
};
*/
 
  const handleNext = () => {
    if (textAnswer) {
      handleAnswer(textAnswer);
    }
    if (currentQuestion < currentQuestions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
      setTextAnswer('');
    } else {
      setScreen('summary');
    }
  };
 


  const handleBack = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(currentQuestion - 1);
    }
  };


  const renderSummary = () => {
    return (
      <View style={styles.summaryContainer}>
        <Text style={styles.summaryTitle}>Quiz Summary</Text>
 
        {Object.values(answers).map((response, index) => ( <Text key={index} style={styles.summaryText}> Question {index + 1}: {response} </Text> ))}
        {/* Button to trigger result submission */}
        <TouchableOpacity style={styles.quizButton} onPress={handleSubmit}>
          <Text style={styles.buttonText}>Submit for Prediction</Text>
        </TouchableOpacity>
 
        {/* Display prediction result */}
        {prediction && (
          <View style={styles.predictionContainer}>
            <Text style={styles.predictionText}>Prediction Result: {prediction}</Text>
          </View>
        )}
 
        {/* Button to go back to the home screen */}
        <TouchableOpacity style={styles.quizButton} onPress={() => setScreen('home')}>
          <Text style={styles.buttonText}>Back to Home</Text>
        </TouchableOpacity>
      </View>
    );
  };
 


const [prediction, setPrediction] = useState(null);  // New state for storing prediction


const handleSubmit = async () => {
  try {
    const response = await fetch("http://192.168.68.126:5000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        disease: diseaseMap[selectedDisease], // Send selected disease type
        answers: answers, // Send the user's answers
      }),
    });


    const data = await response.json();
    setPrediction(data.prediction);  // Set the received prediction to state
  } catch (error) {
    console.error("Error:", error);
    Alert.alert("Error", "Failed to get prediction");
  }
};




return (
  <TouchableWithoutFeedback onPress={() => Keyboard.dismiss()}>
    <ScrollView contentContainerStyle={styles.container}>
      {screen === 'home' ? (
        <>
          <Text style={styles.title}>Take Your Quiz</Text>
          <View style={styles.quizContainer}>
            {Object.keys(questionsMap).map((disease) => (
              <TouchableOpacity key={disease} style={styles.quizButton} onPress={() => handleDiseaseSelection(disease)}>
                <Text style={styles.buttonText}>{disease}</Text>
              </TouchableOpacity>
            ))}
          </View>
        </>
      ) : screen === 'modeSelection' ? (
        <>
          <TouchableOpacity style={styles.homeIcon} onPress={() => setScreen('home')}>
            <Ionicons name="home" size={30} color="#FFF" />
          </TouchableOpacity>
          <Text style={styles.title}>Select Mode</Text>
          <TouchableOpacity style={styles.quizButton} onPress={() => handleQuizStart('Normal')}>
            <Text style={styles.buttonText}>Normal</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.quizButton} onPress={() => handleQuizStart('Short')}>
            <Text style={styles.buttonText}>Short</Text>
          </TouchableOpacity>
        </>
      ) : screen === 'summary' ? (
        renderSummary()
      ) : (
        <>
          <TouchableOpacity style={styles.homeIcon} onPress={() => setScreen('home')}>
            <Ionicons name="home" size={30} color="#FFF" />
          </TouchableOpacity>
          <Text style={styles.questionNumber}>{currentQuestion + 1}/{currentQuestions.length}</Text>
          <Text style={styles.questionText}>{currentQuestions[currentQuestion].text}</Text>
          {currentQuestions[currentQuestion].text.toLowerCase().includes("How old are you?", "rank", "BMI", "mmHg", "mg/dL", "maximum", "depression") ? (
            <TextInput
              style={styles.ageInput}
              placeholder="Enter your answer"
              keyboardType="numeric"
              value={age}
              onChangeText={(text) => {
                if (/^\d*$/.test(text)) setAge(text);
              }}
              placeholderTextColor="#000"
            />
          ) : currentQuestions[currentQuestion].options ? (
            <View style={styles.optionsContainer}>
              {currentQuestions[currentQuestion].options.map((option, index) => (
                <TouchableOpacity
                  key={`${option}-${index}`}
                  style={styles.optionButton}
                  onPress={() => { handleAnswer(option); handleNext(); }}
                >
                  <Text style={styles.optionText}>{option}</Text>
                </TouchableOpacity>
              ))}
            </View>
          ) : (
            <TextInput
              style={styles.ageInput}
              placeholder="Enter your answer"
              keyboardType="numeric"
              value={textAnswer}
              onChangeText={(text) => setTextAnswer(text)}
              placeholderTextColor="#000"
            />
          )}

          <View style={styles.navigationButtons}>
            <TouchableOpacity style={styles.navButton} onPress={handleBack}>
              <Text style={styles.buttonText}>Back</Text>
            </TouchableOpacity>
            <TouchableOpacity style={styles.navButton} onPress={handleNext}>
              <Text style={styles.buttonText}>Next</Text>
            </TouchableOpacity>
          </View>
        </>
      )}
    </ScrollView>
  </TouchableWithoutFeedback>
);
}



const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#000' },
  title: { fontSize: 24, fontWeight: 'bold', color: '#FFF', marginBottom: 40 },
  quizContainer: { width: '80%', flexDirection: 'row', flexWrap: 'wrap', justifyContent: 'space-between' },
  quizButton: { width: '48%', backgroundColor: '#FFF', padding: 20, borderRadius: 10, alignItems: 'center', marginBottom: 10 },
  buttonText: { fontSize: 16, fontWeight: 'bold', color: '#000', textAlign: 'center' },
  questionNumber: { fontSize: 14, color: '#FFF', marginBottom: 5 },
  questionText: { fontSize: 22, fontWeight: 'bold', color: '#FFF', textAlign: 'center', marginBottom: 30 },
  optionsContainer: { width: '80%' },
  optionButton: { backgroundColor: '#FFF', padding: 15, marginVertical: 10, borderRadius: 10, alignItems: 'center' },
  optionText: { fontSize: 18, fontWeight: 'bold', color: '#000' },
  navigationButtons: { flexDirection: 'row', justifyContent: 'space-between', width: '80%', marginTop: 20 },
  navButton: { backgroundColor: '#888', padding: 10, borderRadius: 10, width: '45%', alignItems: 'center' },
  ageInput: { backgroundColor: '#FFF', color: '#000', width: '80%', padding: 10, borderRadius: 10, textAlign: 'center', fontSize: 18, marginVertical: 10 },
  homeIcon: { position: 'absolute', top: 40, left: 20 },
  summaryContainer: { flex: 1, justifyContent: 'center', alignItems: 'center', padding: 20, backgroundColor: '#000' },
  summaryTitle: { fontSize: 24, fontWeight: 'bold', color: '#FFF', marginBottom: 20 },
  summaryText: { fontSize: 16, color: '#FFF', marginBottom: 10, textAlign: 'left', width: '100%' },
  predictionContainer: {
    marginTop: 20,
    backgroundColor: '#4CAF50',
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
    width: '80%',
  },
  predictionText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#FFF',
  },


});

