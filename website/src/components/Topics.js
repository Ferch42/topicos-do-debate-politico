import firebase from 'firebase';

import React from 'react';
import ReactWordcloud from 'react-wordcloud';

import 'tippy.js/dist/tippy.css';
import 'tippy.js/animations/scale.css';

import Slider from '@material-ui/core/Slider';

import { Bubble } from 'react-chartjs-2';


const options = {

  animation: {
        duration: 0, // general animation time
  },
  hover: {
        animationDuration: 0, // duration of animations when hovering an item
  },
  responsiveAnimationDuration: 0, // animation duration after a resize
  scales: {
    yAxes: [
      {
        ticks: {
          beginAtZero: true,
        },
      },
    ],
  },
};



const dates = ['2019-01-01T00:00', '2019-02-01T00:00', '2019-03-01T00:00', '2019-04-01T00:00', '2019-05-01T00:00', '2019-06-01T00:00', '2019-07-01T00:00', '2019-08-01T00:00', '2019-09-01T00:00', '2019-10-01T00:00', '2019-11-01T00:00', '2019-12-01T00:00', 
               '2020-01-01T00:00', '2020-02-01T00:00', '2020-03-01T00:00', '2020-04-01T00:00', '2020-05-01T00:00', '2020-06-01T00:00', '2020-07-01T00:00', '2020-08-01T00:00', '2020-09-01T00:00', '2020-10-01T00:00', '2020-11-01T00:00', '2020-12-01T00:00', 
               '2021-01-01T00:00', '2021-02-01T00:00', '2021-03-01T00:00', '2021-04-01T00:00', '2021-05-01T00:00', '2021-06-01T00:00', '2021-07-01T00:00', '2021-08-01T00:00', '2021-09-01T00:00', '2021-10-01T00:00', '2021-11-01T00:00', '2021-12-01T00:00', 
               '2022-01-01T00:00', '2022-02-01T00:00', '2022-03-01T00:00', '2022-04-01T00:00', '2022-05-01T00:00', '2022-06-01T00:00', '2022-07-01T00:00', '2022-08-01T00:00', '2022-09-01T00:00', '2022-10-01T00:00', '2022-11-01T00:00', '2022-12-01T00:00'
              ,'2023-01-01T00:00']; 

const months = ["JAN", "FEV", "MAR", "ABR", "MAI","JUN", "JUL", "AGO", "SET", "OUT", "NOV", "DEZ"]; 
const marks = [
  {
    value: 0,
    label: '01/2019',
  },
  {
    value: 6,
    label: '07/2019',
  },
  {
    value: 12,
    label: '01/2020',
  },
  {
    value: 18,
    label: '07/2020',
  },
  {
    value: 24,
    label: '01/2021',
  },
  {
    value: 30,
    label: '07/2021',
  },
  {
    value: 36,
    label: '01/2022',
  },
  {
    value: 42,
    label: '07/2022',
  },
  {
    value: 48,
    label: '01/2023',
  },
];


function valuedateFormat(value){
  return months[value%12];
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


const topicColours =  ['#F4ECC2', '#D1F4C2', '#C2F4DD', '#C2E0F4', '#CFC2F4', '#F4C2EE', '#F4C2C3']

function parseTopicIntoPlot(topicData){


      var topicPlotData = { datasets : []}
      var topicsWordData = []
      var availableTopic = 0;

      for(let j = 0; j< 7; j++){
        topicPlotData.datasets.push({
          label: (j+1).toString(),
          data: [],
          //pointRadius: topicSize,
          //pointHoverRadius: topicSize,
          backgroundColor: topicColours[j%7],
        });
        topicsWordData.push([]);
      }
      for(let i = 0; i<20; i++){
        var topicSize =  Math.ceil(topicData[i]['distribuicaoMedia']*750);
        var topicGroupId = topicData[i]['grupoTopico'];

        topicsWordData[topicGroupId].push(topicData[i]['palavras']);
        topicPlotData.datasets[topicGroupId].data.push(
          {x : topicData[i]['tsneCoords'][0], 
           y : topicData[i]['tsneCoords'][1], 
           r : topicSize
          });
        availableTopic = topicGroupId;
      }

      console.log(topicsWordData);
      return [topicPlotData, topicsWordData, availableTopic];

}

// Initialize Firebase
firebase.initializeApp(firebaseConfig);
firebase.analytics();

var db = firebase.firestore();

function Topics() {


  const [dateRange, setDateRange] = React.useState([0, 2]);
  
  // this variable sets the topics for the current date range
  const [topic, setTopic] = React.useState([0,0]);

  const [topicWords, setTopicWords] = React.useState([]);

  const [topicsData, setTopicsData] = React.useState([]);

  const [topicPlotData, setTopicPlotData] = React.useState({});
  
  const handleDateRangeChange = React.useCallback((event, newDateRange) => {
    console.log(dates[newDateRange[0]], dates[newDateRange[1]]);
    setDateRange(newDateRange);
  });

  const updateTopics = React.useCallback(() =>{

  db.collection("topicos").where("dataInicio", "==", dates[dateRange[0]]).where("dataFim", "==", dates[dateRange[1]]).get()
  .then((snapshot) => snapshot.forEach((doc) => {
    if(doc.exists){
        var topics_data = doc.data()['topicos'];

        var [tpd, twd, atopic] = parseTopicIntoPlot(topics_data);
        console.log(twd);
        setTopic([atopic,0]);
        setTopicWords(twd[atopic][0]);
        setTopicsData(twd);
        setTopicPlotData(tpd);
    }
  }))
  .catch((err) => {console.log(err)});
  
  });
  React.useEffect(updateTopics, [dateRange]);

  const change_topic = React.useCallback((el) => {
      
      console.log(el);
    if(el[0]){
      setTopic([el[0].datasetIndex, el[0].index]);
      setTopicWords(topicsData[el[0].datasetIndex][el[0].index]);
    }
  });

  const abacaxi = React.useCallback(() => {
    setTopicWords([1]);
  });

  const options2 = {
   fontSizes: [40, 60],
   enableOptimizations :true,
   rotations: 0
 };
  if(topicWords.length ===0){
    return (
     <div className="content-center">
      <h1> Não há dados para esse intervalo </h1>

      <button onClick={abacaxi}>Click Me</button>;
    </div>
    
    );
  }

  else{
    return (
      <section className="text-gray-600 body-font">
        <div className="container px-5 py-24 mx-auto">
          <div className="flex flex-wrap w-full mb-20">
            <div className="lg:w-1/2 w-full mb-6 lg:mb-0">
              <h1 className="sm:text-3xl text-2xl font-medium title-font mb-2 text-gray-900">Tópicos do Congresso nacional</h1>
              <div className="h-1 w-21 bg-green-500 rounded"></div>
            </div>
            <p className="lg:w-1/2 w-full leading-relaxed text-gray-500">Whatever cardigan tote bag tumblr hexagon brooklyn asymmetrical gentrify, subway tile poke farm-to-table. Franzen you probably haven't heard of them man bun deep jianbing selfies heirloom prism food truck ugh squid celiac humblebrag.</p>
          </div>
          <div class="flex flex-wrap -mx-4 -mb-10 text-center">
            <Slider
                  value={dateRange}
                  onChange={handleDateRangeChange}
                  valueLabelDisplay="auto"
                  min={0}
                  max={48}
                  step={1}
                  marks={marks}
                  aria-labelledby="range-slider"
                  valueLabelFormat={valuedateFormat}
                />
            <div className="sm:w-1/2 mb-10 px-4">
              <div className="bg-gray-100 p-6 rounded-lg"> 
              <div className="rounded-lg h-64 overflow-visible">
                <Bubble data={topicPlotData} getElementAtEvent={change_topic} options={options}/>
              </div>
                <h2 className="title-font text-2xl font-medium text-indigo-500 mt-6 mb-3">Buy YouTube Videos</h2>
               <p className="text-base">Williamsburg occupy sustainable snackwave gochujang. Pinterest cornhole brunch, slow-carb neutra irony.</p>
              </div>
              
             
            </div>
            <div className="sm:w-1/2 mb-10 px-4">
            <div className="bg-gray-100 p-6 rounded-lg">
              <div className="rounded-lg h-64 overflow-visible">
                <ReactWordcloud words={topicWords} options={options2}/>
              </div>
              <h2 className="title-font text-2xl font-medium text-gray-900 mt-6 mb-3">Buy YouTube Videos</h2>
              <p className="text-base">Williamsburg occupy sustainable snackwave gochujang. Pinterest cornhole brunch, slow-carb neutra irony.</p>
            </div>
            </div>
          </div>
        </div>
      </section>
  );
  }
  
}

export default Topics;
