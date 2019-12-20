import React, { useState } from 'react';
import '../stylesheets/Question.css';

export default props => {
    const { question, answer, category, difficulty } = props;
    const [isVisibleAnswer, setVisibleAnswer] = useState(false);

    const toggleVisibleAnswer = () => setVisibleAnswer(!isVisibleAnswer);

    return (
        <div className="Question-holder">
            <div className="Question">{question}</div>
            <div className="Question-status">
                <img className="category" src={`${category}.svg`} alt="category"/>
                <div className="difficulty">Difficulty: {difficulty}</div>
                <img
                    src="delete.png"
                    className="delete"
                    onClick={() => this.props.questionAction('DELETE')}
                    alt="delete"
                />

            </div>
            <div className="show-answer button" onClick={toggleVisibleAnswer}>
                {isVisibleAnswer ? 'Hide' : 'Show'} Answer
            </div>
            <div className="answer-holder">
                <span style={{ "visibility": isVisibleAnswer ? 'visible' : 'hidden' }}>Answer: {answer}</span>
            </div>
        </div>
    );
};
