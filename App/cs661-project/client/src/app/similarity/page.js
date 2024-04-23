'use client'
import React, { Component } from 'react';

import Toolbox from './Toolbox.js';
import Matrix from './Matrix.js';
import { Diagonal } from './utils.js';
import DummyMatrix from './DummyMatrix.js';
import LyricsPane from './LyricsPane.js';
import SongSelector from './SongSelector.js';
import LyricsEditor from './LyricsEditor.js';
import {CustomVerse} from './verse.js';
import { MODE, CUSTOM_SLUG, NOINDEX } from './constants.js';
import config from './config.js';
import CANNED_SONGS from './canned-data.js';

import './page.css';


const MOBILE_THRESH = 768;


// TODO: Would be kind of nice to refactor this into two components.
// An outer component responsible for fetching verses when the path
// changes and showing loading screen when in limbo (having verse 
// as a state variable, like here), and an inner
// component that always has a verse (as a prop). 
// Cause this component has too much going on, and it's ugly having to 
// constantly check whether state.verse is undefined.
class Songsim extends Component {
  constructor(props) {
    super(props);
    // this.db = new DBHelper();
    this.state = {
      matrix_focal: {x: NOINDEX, y: NOINDEX},
      lyrics_focal: NOINDEX,
      mode: config.default_mode,
      ignore_singletons: config.default_ignore_singletons,
      ignore_stopwords: config.stopwords,
      editing: false,
    };
    this.bornMobile = this.state.mobile;
    var verse = this.getVerse();
    this.state['verse'] = verse;
  }
  

  shouldDefaultMobileMode() {
    return 800 < MOBILE_THRESH;    
  }

  componentWillReceiveProps(nextProps) {
    
    // new songid
    // update verse
    var verse = this.getVerse(nextProps);
    // and clear any old highlighting
    this.setState({verse: verse, matrix_focal: {x: NOINDEX, y:NOINDEX},
      lyrics_focal: NOINDEX, editing: false});

  }
  
  // TODO: make this return a promise or something
  /** Fetches an initial verse corresponding to the given props (i.e. the URL).
   * If possible, return the appropriate verse immediately. Otherwise, return
   * a dummy value and asynchronously request the corresponding data, and then
   * set the verse state when it's ready.
   */
  getVerse(props) {
    props = props || this.props;
    // Four possibilities wrt URL:
    // - /custom/[key] : firebase key
    // - /custom       : blank custom verse
    // - /             : default landing song (return it immediately)
    // - /[slug]       : canned song slug
    
      // We don't allow editing in mobile mode. Cause I was too lazy to build the UI.
      if (this.state.mobile) {
        // hacky hack hack hack
        setTimeout(() => {
          this.props.router.replace('/');
        }, 0);
        return;
      }
      // this.verse.set
      var text = `দুলছে হাওয়ায় , না না না ফুল নয়

      দখিনা বাতাসে নাগপাশে সময় নয়।

      খোলা বারান্দায়, এই নির্জনতায়

      সিলিংয়ের বন্ধনে, মাটির ব্যাবধানে

      দুলছে স্খলিত বসনা

      নীলাঞ্জনা নীলাঞ্জনা ।।

      প্রেমিকের স্পর্শ

      আনবেনা শিহরন আর ঐ মনে,

      কেয়ার অফ ফুটপাত নচিকেতা দুটি হাত

      শূণ্যে ছুড়বে ফাঁকা আস্ফালনে,

      উড়ছে মাছি , না না না অবুঝ নয়

      সে আজো একা তাই ঘিরে মাছিরাই রয় ।

      খোলা বারান্দায়, এই নির্জনতায়

      সিলিংয়ের বন্ধনে, মাটির ব্যাবধানে

      দুলছে স্খলিত বসনা

      নীলাঞ্জনা নীলাঞ্জনা ।।

      লাশকাটা ঘরে যদি

      চেরা হয় তার বুক সঙ্গোপনে,

      দেখবে সেখানে রাখা বিবর্ণ

      একমুঠো স্বপ্ন যতনে ।

      যে স্বপ্ন কোন কিশোরের দেয়া উপহার গানের ভাষায় ,

      যে স্বপ্ন প্রথাগত মিথ্যে কপট সংসারের আশায়।

      এখন সময় না না না রাত্রি নয়

      সে আজ জীবনরাত্রি পেরিয়ে গেছে হায় ।।

      খোলা বারান্দায়, এই নির্জনতায়

      সিলিংয়ের বন্ধনে, মাটির ব্যাবধানে

      দুলছে স্খলিত বসনা

      নীলাঞ্জনা নীলাঞ্জনা ।।`;
      return new CustomVerse(text);
  }

  onTextChange = (verse) => {
    let state = {verse: verse};
    if (verse.isCustom() && this.state.mode === MODE.color_title) {
        state['mode'] = config.default_mode;
    }
    this.setState(state);
  }

  // TODO: sort of confusingly named at this point
  makePermalink = () => {
    console.assert(this.state.verse.isCustom() && !this.state.verse.key);
    var ref = this.db.push(this.state.verse);
    this.setState(prevState => ({
      verse: new CustomVerse(prevState.verse.raw, ref.key)
    }));
    // should this also change the URL? Probably easier to say that
    // if you have a firebase key in the URL (i.e. you presumably had this
    // link shared from someone), the text should be immutable, and if 
    // url=custom, it's mutable. 
  }

  /** Only used to generate SVGs for gallery. Super hacky. **/
  batchExportSVGs = (max) => {
    let zip = new JSZip();
    let i = 0;
    let dur = 3000;
    for (let canned of CANNED_SONGS) {
      window.setTimeout(() => {
      SongSelector.loadSong( (verse) => {
        this.setState({verse: verse});
      }, canned);
      }, i*dur);
      window.setTimeout(() => {
        var svg = this.matrix.getSVG();
        zip.file(canned.slug + '.svg', svg);
      }, i*dur+ (dur/2));
      i++;
      if (i >= max) {
        break;
      }
    }
    window.setTimeout(() => {
      zip.generateAsync({type:'blob'}).then( (c) => {
        saveAs(c, 'matrices.zip');
      });
    }, dur * Math.min(max, CANNED_SONGS.length));
  }

  get focal_rowcols() {
    if (!config.alleys) {
      return [undefined, undefined];
    }
    if (this.state.lyrics_focal !== NOINDEX) {
      var thing = [this.state.lyrics_focal, this.state.lyrics_focal];
      return [thing, thing];
    }
    if (this.state.matrix_focal.x !== NOINDEX) {
      var diag = this.focal_local_diag;
      return [diag.yrange, diag.xrange];
    }
    return [undefined, undefined];
  }

  get focal_local_diag() {
    if (this.state.matrix_focal.x === NOINDEX) {
      return undefined;
    }
    var matrix = this.state.verse.matrix;
    return matrix.local_diagonal(
        this.state.matrix_focal.x, 
        this.state.matrix_focal.y
    );
  }

  /** Return a map of diagonals to labels
   */
  get focal_diags() {
    var foc = new Map();
    if (this.state.matrix_focal.x === NOINDEX) {
      return foc;
    }
    // this is kinda dumb but whatever
    var seen = new Set();
    var add = (diag, label) => {
      let k = diag.key;
      if (!seen.has(k)) {
        foc.set(diag, label);
        seen.add(k);
      }
    }
    var primary = this.focal_local_diag;
    add(primary, 'primary');
    for (let correl of primary.mainCorrelates()) {
      add(correl, 'primary-maindiag');
    }
    for (let correl of this.state.verse.matrix.incidental_correlates(primary)) {
      add(correl, 'incidental');
    }

    if (config.checkerboard) {
      var indices = new Set();
      for (let diag of foc.keys()) {
        indices.add(diag.x0);
        indices.add(diag.y0);
      }
      for (let x0 of indices) {
        for (let y0 of indices) {
          add(Diagonal.fromPointAndLength(x0, y0, primary.length),
              'incidental');
        }
      }
    }
    return foc;
  }

  get lyrics_highlights() {
    var hl = new Map();
    var lindex = this.state.lyrics_focal;
    if (lindex !== NOINDEX) {
      hl.set(lindex, 'focal');
      for (let j of this.state.verse.matrix.matches_for_index(lindex)) {
        hl.set(j, 'incidental');
      }
    } else if (this.state.matrix_focal.x !== NOINDEX) {
      // Focal rect
      hl.set(this.state.matrix_focal.x, 'focal');
      hl.set(this.state.matrix_focal.y, 'focal');
      // This is lazy, but should basically work for now
      for (let [diag, strength] of this.focal_diags) {
        for (let [x, _y] of diag.points()) {
          if (!hl.has(x)) {
            hl.set(x, strength);
          }
        }
      }
    }
    return hl;
  }

  matrix_hover_cb = (pt) => {
    this.setState({matrix_focal: pt})
  }
  
  // Called then the new/edit button is clicked.
  onEditButton = () => {
    if (this.state.verse.isCustom()) {
      this.setState({editing: true});
    } else {
      hashHistory.push(CUSTOM_SLUG); 
    }
  }

  // This thing sort of defies separation of concerns, 
  // but it also means writing less boilerplate code, sooooo
  stateChanger = (state) => {
    this.setState(state);
  }

  // renderBrowserWarning() {
  //   if (browser.name && browser.name !== 'chrome') {
  //     return (<p className="bg-danger"><b>Warning:</b> This site runs best on Chrome. It may run slowly on other browsers, or not at all.</p>);
  //   }
  // }

  render() {
    // TODO: this method is getting pretty huge
    var rowcols = this.focal_rowcols;
    var rows = rowcols[0], cols = rowcols[1];
    var matrix;
    if (!this.state.verse) {
      matrix = <DummyMatrix />;
    } else {
      // TODO: probably passing way more props than necessary at this point
      matrix = (
        <Matrix 
          verse={this.state.verse} 
          hover_cb={this.matrix_hover_cb}
          focal_rows={rows}
          focal_cols={cols}
          matrix_focal={this.state.matrix_focal}
          lyrics_focal={this.state.lyrics_focal}
          focal_diags={this.focal_diags}
          mode={this.state.mode}
          ignore_singletons={this.state.ignore_singletons}
          stopwords={this.state.ignore_stopwords}
          ref={(m) => {this.matrix = m}}
        />
      );
    }
    var debug;
    // TODO: debug component?
    if (config.debug && this.state.verse) {
      var rects = Array.from(this.state.verse.rects());
      debug = (<div>
          <p>
          {this.state.verse.matrix.length} x {this.state.verse.matrix.length}{", "} 
          {rects.length} rects
          </p>
          <p>Custom: {JSON.stringify(this.state.verse.isCustom())}</p>
          <button onClick={()=>(this.batchExportSVGs(11222))}>
            Batch export (SLOW)
          </button>
          <button onClick={()=>(this.batchExportSVGs(4))}>
            Mini batch export (only a little SLOW)
          </button>
          <a href={this.props.router.createHref('custom/' + config.testingFBKey)}>
            Custom song.
          </a>
        </div>);
    }
    var dfm;
    var h = 1280;
    var w = 720;
    var mindim = Math.min(h, w);
    if (this.state.mobile) {
      dfm = Math.min(768, mindim * .9); // testing
    } else {
      dfm = Math.min(w * .45, h*.8);
    }
    var defaultMatrixSize = dfm; // TODO: have this flow from above (and calculate from screen.height or something)
    matrix = (
          <div className='matrixdiv'
            >
              {matrix}
          </div>
    );
    var toolbox = (
      <Toolbox
        verse={this.state.verse}
        mode={this.state.mode}
        ignoreSingletons={this.state.ignore_singletons}
        ignore_stopwords={this.state.ignore_stopwords}
        mobile={this.state.mobile}
        onStateChange={this.stateChanger}
        exportSVG={() => (this.matrix && this.matrix.exportSVG())}
        onShare={this.makePermalink}
        router={this.props.router}
      />
    );
    
    var lyrics;
    if (this.state.verse && (this.state.verse.isBlank() || this.state.editing)) {
      lyrics = (
          <LyricsEditor
            verse={this.state.verse}
            onChange={this.onTextChange}
            onStateChange={this.stateChanger}
          />);
    } else {
      lyrics = (
        <LyricsPane verse={this.state.verse || CustomVerse.BlankVerse()} 
          loading={!this.state.verse}
          hover_cb={(i) => this.setState({lyrics_focal: i})}
          highlights={this.lyrics_highlights}
          onEditButton={this.onEditButton}
        />);
    }
    return (
      <div>
        <div className="container-fluid mainContainer flex">
          <div className="matrixPane matrixdiv">
            {matrix}
          </div>
          <div className="lyricsPane">
              <SongSelector
                selected={this.state.verse && this.state.verse.id}
                onEdit={this.onEditButton}
                onChange={this.onTextChange}
                onStateChange={this.stateChanger}
              />
              {lyrics}
          </div>
        </div>
        <div className="container">
          {toolbox}
        </div>
        {debug}
        </div>
        );
  }

}

export default Songsim;