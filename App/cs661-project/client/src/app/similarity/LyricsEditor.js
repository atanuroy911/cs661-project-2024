'use client'
import React, { Component } from 'react';

import './LyricsPane.css';

import {CustomVerse} from './verse.js';

class LyricsEditor extends Component {
  
  textAreaBlur = (e) => {
    // When the textarea loses focus, treat this as an intent to save unless
    // the thing gaining focus is the "cancel" button.
    if (e.relatedTarget && e.relatedTarget.id === "cancelEdit") {
      return;
    }
    if (this.ta.value.length === 0) {
      if (this.props.verse.isBlank()) {
        // Do nothing
        return;
      } else {
        this.abortEditing();
      }
    } else {
      this.onTextEdit();
      this.abortEditing();
    }
  }

  onTextEdit = () => {
    if (!this.props.verse.isCustom()) {
      console.error("Tried to edit a song that shouldn't be editable. Bailing.");
      return;
    }
    if (this.ta.value === this.props.verse.raw) {
      return;
    }
    var verse = new CustomVerse(this.ta.value);
    this.props.onChange(verse);
  }

  // Abort without saving changes
  abortEditing = () => {
    this.props.onStateChange({editing: false});
  }

  componentDidMount() {
    this.ta.focus();
  }

  render() {
    var showCancel = !this.props.verse.isBlank();
    return (
      <div>
        <textarea 
        className="form-control lyrics"
        defaultValue={this.props.verse.raw} 
        onBlur={this.textAreaBlur}
        ref={(ta) => {this.ta = ta}}
        />
        
        <button className="btn text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800" onClick={this.onTextEdit}>Save</button>
        {/* TODO: clicking cancel when the textarea is empty should either
            a) Jump to the default landing song, or
            b) (Preferably) go back to the last viewed canned song.
            (Assuming there was no content previously. If there was, it should 
             be resurrected.) */}
        {showCancel &&
          <button id="cancelEdit" className="btn focus:outline-none text-white bg-red-700 hover:bg-red-800 focus:ring-4 focus:ring-red-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-red-600 dark:hover:bg-red-700 dark:focus:ring-red-900" 
            onClick={this.abortEditing}
          >
            Cancel
          </button>
        }
      </div>
    );
  }
}

export default LyricsEditor;
