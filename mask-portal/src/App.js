import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Switch, Redirect, NavLink } from "react-router-dom";

import Home from "./pages/Home";
import Masks from "./pages/Masks";
import Images from "./pages/Images";

import './App.css';

class App extends Component {
  render() {
    return (
      <Router>
        <div className="App">
          <div className='header'>
            <NavLink
              exact={true}
              to={`/`}
              activeClassName="active"
              className="nav-selection primary"
            >
              MeRiT Monitor
            </NavLink>
            <NavLink
              exact={true}
              to={`/masks/`}
              activeClassName="active"
              className="nav-selection"
            >
              Masks
            </NavLink>
            <NavLink
              exact={true}
              to={`/images/`}
              activeClassName="active"
              className="nav-selection"
            >
              Images
            </NavLink>
          </div>
          <div className='content'>
            <Switch>
              <Route path="/" exact component={Home} />
              <Route path="/masks/" exact component={Masks} />
              <Route path="/images/" exact component={Images} />
              <Redirect to="/" />
            </Switch>
          </div>
        </div>
      </Router>
    );
  }
}

export default App;
