import React from 'react';
import '../stylesheets/Header.css';

export default () => {

    const navTo = uri => {
        window.location.href = window.location.origin + uri;
    };

    const routes = {
        List: '',
        Add: '/add',
        Play: '/play',
    };

    return (
        <div className="App-header">
            <h1 onClick={() => {navTo('')}}>Udacitrivia</h1>
            {Object.key(routes).map(key => <h2 key={key} onClick={() => {navTo(routes[key])}}>{key}</h2>)}
        </div>
    );
};
