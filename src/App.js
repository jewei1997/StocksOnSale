import React from 'react';
import './App.css';
import { Table } from 'react-bootstrap';

class App extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      tickers: [],
      pe_ratios: [],
    }
  }

  async componentDidMount() {
    const response = await fetch(`/stocks/pe_ratios/`);
    const json = await response.json();
    this.setState({tickers: json["tickers"], pe_ratios: json["pe_ratios"]})
  }

  render() {
    const len = this.state.tickers.length
    return (
        <Table striped bordered hover variant="dark">
          <thead>
          <tr>
            <th>Ticker</th>
            <th>PE Ratio</th>
          </tr>
          </thead>
          <tbody>
          {Array.from({length: len}).map((_, index) => {
            const ticker = this.state.tickers[index];
            const pe_ratio = this.state.pe_ratios[index];
            return (
                <tr>
                  <td key={index}><a
                      href={'https://finance.yahoo.com/quote/' + ticker}>{ticker}</a>
                  </td>
                  <td key={len + index}>{pe_ratio}</td>
                </tr>
            )
          })}
          </tbody>
        </Table>
    )
  }
}

export default App;
