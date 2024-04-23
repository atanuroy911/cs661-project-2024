'use client'
import React, { Component } from 'react';
// import Clipboard from 'clipboard';

import './Toolbox.css';

import config from './config.js';
import { MODE, MODE_TOOLTIPS } from './constants.js';

// TODO: is this really the orthodox way to do this? :/
// new Clipboard('#perma');

/**
 * Contains a bunch of controls for stuff like:
 * - setting matrix coloring mode
 * - whether to ignore singletons
 * - saving svg file
 * - sharing/permalinks
 * Separating this stuff into a component separate from Songsim involves some
 * spooky action at a distance, but I think it's worth it to simplify Songsim,
 * particularly its render method.
 */
class Toolbox extends Component {

  renderModeRadio = (mode_key) => {
    var mode = MODE[mode_key];
    var tt = MODE_TOOLTIPS[mode_key];
    // TODO: Really when we get a change to state.verse, we should see if
    // the new verse is custom && mode is color_title, and if so, we should
    // automatically switch to a different mode. But bleh.
    var disabled = (mode === MODE.color_title &&
      (!this.props.verse || !this.props.verse.title));
    var divCname = disabled ? "mr-2 radio-inline disabled" : "mr-2 radio-inline";
    return (
      <label title={tt} key={mode} className={divCname}>
        <input type="radio"
          disabled={disabled}
          checked={this.props.mode === mode}
          value={mode}
          onChange={(e) => {
            this.props.onStateChange({ mode: e.target.value })
          }}
          name="mode" />
        {mode}
      </label>
    );
  }

  renderSingletonRadios = () => {
    var singstop = [this.props.ignoreSingletons, this.props.ignore_stopwords];
    var modes = [
      { label: 'show all', ss: [false, false] },
      { label: 'ignore all', ss: [true, false] },
      {
        label: 'ignore stopwords', ss: [false, true],
        tt: 'Show single-word matches, unless they\'re common words like "the" or "and"'
      },
    ];
    var radios = [];
    for (let mode of modes) {
      radios.push((
        <label className="radio-inline mr-2" key={mode.label} title={mode.tt}>
          <input type="radio"
            checked={singstop[0] === mode.ss[0] && singstop[1] === mode.ss[1]}
            value={mode.ss}
            onChange={(e) => {
              this.props.onStateChange({
                ignore_singletons: mode.ss[0],
                ignore_stopwords: mode.ss[1]
              });
            }}
          />
          {mode.label}
        </label>
      ));
    }
    return (
      <fieldset>
        <legend title="How to treat individual squares floating off the main diagonal">
          <b>Single-word matches</b>
        </legend>
        {radios}
      </fieldset>
    );
  }

  renderMobileCheckbox = () => {
    return (
      <></>
    );
  }

  renderSave = () => {
    if (!this.props.mobile && this.props.verse && config.exportSVGEnabled
      && this.props.exportSVG) {
      return (
        <button className="btn"
          onClick={this.props.exportSVG}
          title="Save matrix as SVG file"
        >
          <span className="glyphicon glyphicon-save" />
        </button>
      );
    }
  }

  renderPermalink = () => {
    if (this.props.mobile ||
      !(this.props.verse && this.props.verse.isCustom() && !this.props.verse.isBlank())) {
      return;
    }
    var perma = this.props.verse.get_permalink(this.props.router);
    if (perma) {
      return (
        <label className="form-inline">
          Permalink:
          <input
            type="text" readOnly={true}
            value={perma} />
          <button id="perma" className="btn" data-clipboard-text={perma}>
            <span className="glyphicon glyphicon-copy" title="copy" />
          </button>
        </label>
      );
    } else {
      return (
        <button className="btn" onClick={this.props.onShare}
          title="Generate a shareable permalink for this song"
        >
          Permalink
        </button>
      );
    }
  }

  render() {
    var moderadios = Object.keys(MODE).map(this.renderModeRadio);
    var kls = this.props.mobile ? "" : "mr-2 sm:flex sm:flex-row"; // Flex layout for mobile
    kls += ' toolbox';
    kls = 'toolbox'; // Remove unnecessary class
    var radioKls = 'sm:w-1/4 md:w-1/3 lg:w-1/2'; // Column width classes for radios

    return (
      <div className={kls}>
        <div className={radioKls}>
          <fieldset>
            <legend className="text-lg font-bold">Color Mode</legend>
            {moderadios}
          </fieldset>
        </div>
        <div className={radioKls}>
          {this.renderSingletonRadios()}
        </div>

        <div className="sm:w-1/2 md:w-1/4 lg:w-1/6"> {/* Adjust column widths as needed */}
          {this.renderMobileCheckbox()}
        </div>
        <div className="sm:w-1/2 md:w-1/4 lg:w-1/6"> {/* Adjust column widths as needed */}
          {this.renderSave()}
        </div>
      </div>
    );

  }
}


export default Toolbox;
