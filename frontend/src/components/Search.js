import React, { useState } from 'react'

export default () => {

    const [query, setQuery] = useState('');

    const getInfo = event => {
        event.preventDefault();
        this.props.submitSearch(this.state.query)
    };

    return (
        <form onSubmit={getInfo}>
            <input
                placeholder="Search questions..."
                value={query}
                onChange={e => setQuery(e.target.value)}
            />
            <input type="submit" value="Submit" className="button"/>
        </form>
    )
};
