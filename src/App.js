import React from 'react';
import './App.css';
import Table from 'react-bootstrap/Table';
import {arrayToDict, numFormatter, percentFormatter, onSort} from "./Helpers";
import { FaSort } from "react-icons/fa";
import { Button } from 'antd';

import 'bootstrap/dist/css/bootstrap.min.css';


class App extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      // data = [{"ticker": t1, "pe_ratio": pe1, "market_cap": mc1, ...},
      //         {"ticker": t2, "pe_ratio": pe2, "market_cap": mc2, ...},
      //         ...
      //        ]
      data: [],
      is_ascending: true,
    }
  }

  async componentDidMount() {
    const pe_resp = await fetch(`/stocks/pe_ratios/`)
    const pe_json = await pe_resp.json()
    const mc_resp = await fetch(`stocks/market_caps/`)
    const mc_json = await mc_resp.json()
    const pc_week_resp = await fetch(`stocks/percentage_change/7/`)
    const pc_week_json = await pc_week_resp.json()
    const pc_month_resp = await fetch(`stocks/percentage_change/30/`)
    const pc_month_json = await pc_month_resp.json()
    const pc_year_resp = await fetch(`stocks/percentage_change/365/`)
    const pc_year_json = await pc_year_resp.json()

    const tickerToPe = arrayToDict(pe_json.data, "pe_ratio")
    const tickerToMarketCap = arrayToDict(mc_json.data, "market_cap")
    const tickerToWeekPercentageChange = arrayToDict(pc_week_json.data, "percentage_change")
    const tickerToMonthPercentageChange = arrayToDict(pc_month_json.data, "percentage_change")
    const tickerToYearPercentageChange = arrayToDict(pc_year_json.data, "percentage_change")


    // build data so that it looks like:
    // data = [{"ticker": t1, "pe_ratio": pe1, "market_cap": mc1, ...},
    //         {"ticker": t2, "pe_ratio": pe2, "market_cap": mc2, ...},
    //         ...
    //        ]
    let data = []
    for (const ticker in tickerToPe) {
      let data_element = {"ticker": ticker,
                          "pe_ratio": tickerToPe[ticker],
                          "market_cap": tickerToMarketCap[ticker],
                          "week_percentage_change": tickerToWeekPercentageChange[ticker],
                          "month_percentage_change": tickerToMonthPercentageChange[ticker],
                          "year_percentage_change": tickerToYearPercentageChange[ticker],
      }
      data.push(data_element)
    }

    // set data to this.state.data
    this.setState({data: data})
  }

  handleSort(event, sortKey) {
    const data = onSort(event, sortKey, this.state.data, this.state.is_ascending)
    this.state.is_ascending = !this.state.is_ascending
    this.setState({data: data})
  }

  render() {
    const len = (this.state.data === undefined ? 0 : this.state.data.length)
    return (
        <>
        {/*<Button type="primary" style={{color: "black"}}size={"large"}>*/}
        {/*  Primary*/}
        {/*</Button>*/}
        <Table striped bordered hover variant="dark">
          <link
              rel = "stylesheet"
              href = "https://maxcdn.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css"
              integrity = "sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk"
              crossOrigin = "anonymous"
          />
          <thead>
          <tr>
            {/*TODO: can sort by ticker as well!*/}
            <th onClick={e => this.handleSort(e, "ticker")}>Ticker<FaSort/></th>
            <th onClick={e => this.handleSort(e, "pe_ratio")}>PE Ratio<FaSort/></th>
            <th onClick={e => this.handleSort(e, "market_cap")}>Market Cap<FaSort/></th>
            <th onClick={e => this.handleSort(e, "week_percentage_change")}>1 Week<FaSort/></th>
            <th onClick={e => this.handleSort(e, "month_percentage_change")}>1 Month<FaSort/></th>
            <th onClick={e => this.handleSort(e, "year_percentage_change")}>1 Year<FaSort/></th>
          </tr>
          </thead>
          <tbody>
          {Array.from({length: len}).map((_, index) => {
            const stock_data_ele = this.state.data[index]
            const ticker = stock_data_ele["ticker"]
            const pe_ratio = stock_data_ele["pe_ratio"]
            const market_cap = numFormatter(stock_data_ele["market_cap"])
            const week_percentage_change = percentFormatter(stock_data_ele["week_percentage_change"])
            const month_percentage_change = percentFormatter(stock_data_ele["month_percentage_change"])
            const year_percentage_change = percentFormatter(stock_data_ele["year_percentage_change"])
            return (
                <tr>
                  <td key={index}><a href={'https://finance.yahoo.com/quote/' + ticker}>{ticker}</a></td>
                  <td key={len + index}>{pe_ratio}</td>
                  <td key={2*len + index}>{market_cap}</td>
                  <td key={3*len + index} style={{ color: stock_data_ele["week_percentage_change"] > 0.0 ? 'green' : 'red'}}>{week_percentage_change}</td>
                  <td key={4*len + index} style={{ color: stock_data_ele["month_percentage_change"] > 0.0 ? 'green' : 'red'}}>{month_percentage_change}</td>
                  <td key={5*len + index} style={{ color: stock_data_ele["year_percentage_change"] > 0.0 ? 'green' : 'red'}}>{year_percentage_change}</td>
                </tr>
            )
          })}
          </tbody>
        </Table>
        </>
    )
  }
}

export default App;
