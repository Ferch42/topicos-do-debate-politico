import firebase from 'firebase';

import React from 'react';
import ReactWordcloud from 'react-wordcloud';

import 'tippy.js/dist/tippy.css';
import 'tippy.js/animations/scale.css';

import Slider from '@material-ui/core/Slider';

import { Bubble } from 'react-chartjs-2';

import { dates, months, marks, topicColours, firebaseConfig } from '../utils/constants';
import { valuedateFormat } from '../utils/utils';

const options = {
  scales:{
    xAxes: [{
        display: false //this will remove all the x-axis grid lines
    }],
    yAxes: [{
        display: false //this will remove all the x-axis grid lines
    }]
  },
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
            <p className="lg:w-1/2 w-full leading-relaxed text-gray-500">Bem vindo ao Tópicos do Congresso nacional! Defina um intervalo de tempo abaixo e clique em um dos círculos no gráfico para ver os principais tópicos discutidos.</p>
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
                <h2 className="title-font text-2xl font-medium text-indigo-500 mt-6 mb-3">Agrupamento de tópicos</h2>
               <p className="text-base">Acima estão representados os agrupamentos de diferentes tópicos e palavras.</p>
              </div>
              
             
            </div>
            <div className="sm:w-1/2 mb-10 px-4">
            <div className="bg-gray-100 p-6 rounded-lg">
              <div className="rounded-lg h-64 overflow-visible">
                <ReactWordcloud words={topicWords} options={options2}/>
              </div>
              <h2 className="title-font text-2xl font-medium text-gray-900 mt-6 mb-3">Principais palavras</h2>
              <p className="text-base">Acima estão as principais palavras de acordo com o intervalo de tempo selecionado.</p>
            </div>
            </div>
          </div>
        </div>
      </section>
    );
  }
}

export default Topics;
