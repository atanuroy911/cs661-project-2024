'use client'
import React, { Component } from 'react';

import './SongSelector.css';
  
class SongSelector extends Component {


  render() {
    // Apply some different effects to the button next to the dropdown depending
    // on whether we're talking about editing an existing custom song, or starting
    // a new one.
    var is_edit = true;
    var glyph = is_edit ? 'pencil' : 'plus';
    var cust_title = is_edit ? 'Edit song' : 'New song';
    return (
            <div className="form-horizontal songselector">
              <div className="form-group">
              <div className="col-xs-11">
              </div>
              {this.props.allowEdit &&
              <span className="col-xs-1 input-lg">
                <button className="btn" onClick={this.props.onEdit}
                  title={cust_title}
                >
                  <span className={"glyphicon glyphicon-" + glyph} />
                </button>
              </span>
              }
              </div>
            </div>
        );
  }
}


export default SongSelector;
