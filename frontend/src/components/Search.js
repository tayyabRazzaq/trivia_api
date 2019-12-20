import React, { useState } from 'react'

export default ({ submitSearch }) => {

    const [query, setQuery] = useState('');

    const getInfo = event => {
        event.preventDefault();
        submitSearch(query)
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
