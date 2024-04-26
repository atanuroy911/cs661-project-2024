import React, { Component } from 'react';

import './SongSelector.css';

import {CUSTOM_SLUG} from './constants.js';

  
class SongSelector extends Component {

  // TODO: this is basically a static variable 
  renderOptionGroups() {
    var res = [];
    // The first option is a special case: custom song
    if (this.props.allowEdit) {
      var custom = (<option key='custom' value={CUSTOM_SLUG}>Custom</option>);
      res.push(custom);
    }
    return res;
  }

  render() {
    // Apply some different effects to the button next to the dropdown depending
    // on whether we're talking about editing an existing custom song, or starting
    // a new one.
    var is_edit = this.props.selected === CUSTOM_SLUG;
    var glyph = is_edit ? 'pencil' : 'plus';
    var cust_title = is_edit ? 'Edit song' : 'New song';
    return (
            <div className="form-horizontal songselector">
              <div className="form-group">
              <div className="col-xs-11">
              <select className="form-control input-lg" 
                onChange={this.handleChange} value={this.props.selected} >
              {this.renderOptionGroups()}
              </select></div>
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

SongSelector.propTypes = {
  selected: React.PropTypes.string,
  onEdit: React.PropTypes.func,
  allowEdit: React.PropTypes.bool,
};

SongSelector.defaultProps = {
  allowEdit: true,
};

export default SongSelector;
