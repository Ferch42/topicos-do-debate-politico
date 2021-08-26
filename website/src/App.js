import logo from './logo.svg';
import './App.css';

import firebase from 'firebase';

import React from 'react';
import ReactWordcloud from 'react-wordcloud';

import 'tippy.js/dist/tippy.css';
import 'tippy.js/animations/scale.css';


import { makeStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import Slider from '@material-ui/core/Slider';



function valuetext(value) {
  return `${value}°C`;
}



const words = [
  {
    text: 'told',
    value: 64,
  },
  {
    text: 'mistake',
    value: 11,
  },
  {
    text: 'thought',
    value: 16,
  },
  {
    text: 'bad',
    value: 17,
  },
]

function SimpleWordcloud() {
  return <ReactWordcloud words={words} />
}


var firebaseConfig = {
    apiKey: "AIzaSyALw4qoQcmIi-d0seKne9T6BrOQh499ebc",
    authDomain: "politic-topics.firebaseapp.com",
    projectId: "politic-topics",
    storageBucket: "politic-topics.appspot.com",
    messagingSenderId: "523630111752",
    appId: "1:523630111752:web:8f7088b7c8dadb06baf5bd",
    measurementId: "G-VCFESPY9E3"
  };


// Initialize Firebase
firebase.initializeApp(firebaseConfig);
firebase.analytics();

var db = firebase.firestore();

function App() {


  const [value, setValue] = React.useState([20, 37]);

  const handleChange = (event, newValue) => {
    console.log(newValue);
    setValue(newValue);
  };
  return (
    <div className="App">
      <h1>Tópicos do debate político</h1>
      <p>A BA CA XI </p>
      <Slider
        value={value}
        onChange={handleChange}
        valueLabelDisplay="auto"
        step={10}
        marks
        aria-labelledby="range-slider"
        getAriaValueText={valuetext}
      />
      <SimpleWordcloud/>
    </div>
  );
}

export default App;
