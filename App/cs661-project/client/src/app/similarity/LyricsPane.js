'use client'
import React, { Component } from 'react';

import './LyricsPane.css';

import Word from './Word.js';
import { NOINDEX } from './constants.js';

/** Shows the entire current verse in a big multi-column block. Not responsible
 * for the editing view. */
class LyricsPane extends Component {

  renderWord = (word) => {
    return (<Word i={word.i} key={word.i} raw={word.raw} 
                focus={this.props.highlights.get(word.i) || 0} 
                hover_cb={this.props.hover_cb}
            />);
  }

  renderLine = (line, idx) => {
    var words = line.map(this.renderWord);
    var x = [];
    // Hack to put spaces between word spans. We could just put them in the spans
    // themselves, but then we get funny underlining behaviour.
    for (let word of words) {
      x.push(word);
      x.push(" ");
    }
    return <div className="line" key={idx}>{x.slice(0,-1)}</div>;
  }

  componentWillUnmount() {
    this.props.hover_cb(NOINDEX);
  }

  render() {
    var lines = this.props.verse.lines.map(this.renderLine);
    return (
          <div className="words lyrics w-4/5 bg-gray-50 max-h-screen overflow-y-auto text-sm" 
            onClick={this.props.verse && this.props.verse.isCustom() && this.props.onEditButton} 
          >
            {this.props.loading &&
              <h3>Loading...</h3>
            }
            {lines}
          </div>
    );
  }
}


export default LyricsPane;
