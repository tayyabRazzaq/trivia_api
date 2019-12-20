import React, { Component } from 'react';
import $ from 'jquery';

import '../stylesheets/FormView.css';

export default class FormView extends Component {
    constructor(props) {
        super(props);
        this.state = {
            question: '',
            answer: '',
            difficulty: 1,
            category: 1,
            categories: {}
        }
    }

    componentDidMount() {
        $.ajax({
            url: `/categories`,
            type: 'GET',
            success: result => {
                this.setState({ categories: result.categories });
            },
            error: () => {
                alert('Unable to load categories. Please try your request again');
            }
        })
    }


    submitQuestion = event => {
        event.preventDefault();
        $.ajax({
            url: '/questions',
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({
                question: this.state.question,
                answer: this.state.answer,
                difficulty: this.state.difficulty,
                category: this.state.category
            }),
            xhrFields: {
                withCredentials: true
            },
            crossDomain: true,
            success: () => {
                document.getElementById('add-question-form').reset();
            },
            error: () => {
                alert('Unable to add question. Please try your request again');
            }
        })
    };

    handleChange = event => this.setState({ [event.target.name]: event.target.value });

    render() {
        return (
            <div id="add-form">
                <h2>Add a New Trivia Question</h2>
                <form className="form-view" id="add-question-form" onSubmit={this.submitQuestion}>
                    <label>
                        Question
                        <input type="text" name="question" onChange={this.handleChange}/>
                    </label>
                    <label>
                        Answer
                        <input type="text" name="answer" onChange={this.handleChange}/>
                    </label>
                    <label>
                        Difficulty
                        <select name="difficulty" onChange={this.handleChange}>
                            {[1, 2, 3, 4, 5].map(value => <option key={value} value={value}>{value}</option>)}
                        </select>
                    </label>
                    <label>
                        Category
                        <select name="category" onChange={this.handleChange}>
                            {Object.keys(this.state.categories).map(id =>
                                <option key={id} value={id}>{this.state.categories[id]}</option>)}
                        </select>
                    </label>
                    <input type="submit" className="button" value="Submit"/>
                </form>
            </div>
        );
    }
}
