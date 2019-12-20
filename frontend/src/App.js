import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom'
import './stylesheets/App.css';
import { FormView, QuestionView, Header, QuizView } from './components';


export default () => (
    <div className="App">
        <Header path/>
        <Router>
            <Switch>
                <Route path="/" exact component={QuestionView}/>
                <Route path="/add" component={FormView}/>
                <Route path="/play" component={QuizView}/>
                <Route component={QuestionView}/>
            </Switch>
        </Router>
    </div>
);
