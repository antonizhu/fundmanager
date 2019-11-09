Survey
    .StylesManager
    .applyTheme("morden");

var total_score = 41
var json = {
    "pages": [
        {
            "name": "page1",
            "elements": [
                {
                    "type": "radiogroup",
                    "name": "investment_objectives",
                    "title": "Which of the following do you think best describes your investment objectives?",
                    //"isRequired": true,
                    //"hasOther": true,
                    "choices": [
                      {
                          "value": 1,
                          "text": "Your primary focus is on capital growth. You are prepared to accept a high level of short term volatility and possible capital losses in order to generate potentially higher levels of capital growth over the long term. You are well placed to recover from unforeseen market downturns either because you have time on your side or access to capital reserves."
                      }, {
                          "value": 3,
                          "text": "You require your investments to be a balance between capital growth and income generating assets. Calculated risks will be acceptable as you are prepared to accept short term levels of volatility in order to outperform inflation."
                      }, {
                          "value": 5,
                          "text": "Generating a regular income stream is a priority over capital growth. You are prepared to sacrifice higher returns in favour of preservation of capital."
                      }
                    ],
                    //"colCount": 2
                }, {
                    "type": "radiogroup",
                    "name": "risk_capital_percentage",
                    //"visibleIf": "{investment_objectives} != 'Hobbyist'",
                    "title": "What percentage of your risk capital will be put at risk using our services as your broker? (NB: Risk capital means funds and assets which if lost would not materially change your lifestyle or your family’s lifestyle)",
                    //"isRequired": true,
                    "choices": [
                      {
                          "value": 1,
                          "text": "Greater than 70%"
                      }, {
                          "value": 3,
                          "text": "35% to 70%"
                      }, {
                          "value": 5,
                          "text": "Less than 35%"
                      }
                    ]
                }, {
                    "type": "radiogroup",
                    "name": "saving_duration",
                    //"visibleIf": "{investment_objectives} != 'Hobbyist'",
                    "title": "Once investments have been placed, how long would it be before you would need to access your capital?",
                    //"isRequired": true,
                    //"hasOther": true,
                    "choices": [
                      {
                          "value": 1,
                          "text": "Longer than 2 years"
                      }, {
                          "value": 3,
                          "text": "Between 6 months and 2 years"
                      }, {
                          "value": 5,
                          "text": "Less than 6 months"
                      }
                    ]
                    //"colCount": 4
                }
            ]
        }, {
            "name": "page2",
            "elements": [
                {
                    "type": "radiogroup",
                    "name": "inflation_effects",
                    "title": "Inflation can reduce your spending power. How much risk are you prepared to take to counteract the effects of inflation?",
                    //"isRequired": true,
                    //"hasOther": true,
                    "choices": [
                      {
                          "value": 1,
                          "text": "I am comfortable with short to medium term losses in order to beat inflation over the longer term"
                      }, {
                          "value": 5,
                          "text": "I am conscious of the effects of inflation, and am prepared to take moderate risks in order to stay ahead of inflation"
                      }, {
                          "value": 10,
                          "text": "Inflation may erode my savings over the long term, but I am only willing to take limited risk to attempt to counter the effects of inflation"
                      }
                    ]
                    //"otherText": "Other",
                    //"colCount": 3
                },{
                    "type": "radiogroup",
                    "name": "emergencies_saving",
                    "title": "How much money have you set aside (outside of your pension / Central Provident Fund savings) to handle emergencies?",
                    //"isRequired": true,
                    //"hasOther": true,
                    "choices": [
                      {
                          "value": 1,
                          "text": "More than six months of living expenses"
                      }, {
                          "value": 3,
                          "text": "Between one and six months of living expenses"
                      }, {
                          "value": 5,
                          "text": "Less than one month of living expenses"
                      }
                    ],
                    //"choicesOrder": "asc",
                    //"otherText": "Other (Please name it)",
                    //"colCount": 3
                }, {
                    "type": "radiogroup",
                    "name": "asset_mixes",
                    "title": "You possess $100,000 and wish to invest the funds for the future. Which of the asset mixes would you choose to invest in? \n Investment A has a potential return of 30% but the possibility of losing up to 40% in any year. \n Investment B has an average return of 3% with the possibility of losing up to 5% in any year.",
                    //"isRequired": true,
                    //"hasOther": true,
                    "choices": [
                      {
                          "value": 1,
                          "text": "80% in Investment A and 20% in Investment B"
                      }, {
                          "value": 3,
                          "text": "50% in Investment A and 50% in Investment B"
                      }, {
                          "value": 5,
                          "text": "20% in Investment A and 80% in Investment B"
                      }
                    ]
                    //"choicesOrder": "asc",
                    //"otherText": "Other (Please name it)",
                    //"colCount": 3
                }
            ]
        }, {
            "name": "page3",
            "elements": [
                {
                    "type": "radiogroup",
                    "name": "expected_return",
                    "title": ". Over the longer term, what return do you reasonably expect to achieve from your investment portfolio?",
                    //"isRequired": true,
                    "choices": [
                      {
                          "value": 1,
                          "text": "More than 9% per annum above the prevailing fixed deposit rate"
                      }, {
                          "value": 3,
                          "text": "Prevailing fixed deposit rate plus 3-9% per annum"
                      }, {
                          "value": 5,
                          "text": "Less than 3% per annum above the prevailing fixed deposit rate"
                      }
                    ]
                }, {
                    "type": "radiogroup",
                    "name": "investment_fluctuation",
                    //"visibleIf": "{useproduct} = \"Yes\"",
                    "title": "Most investments can fluctuate both up and down (i.e. volatility). How much could your investment fall in value over a 12 month period before you begin to feel concerned and anxious?",
                    //"isRequired": true,
                    "choices": [
                      {
                          "value": 1,
                          "text": "More than 25%"
                      }, {
                          "value": 5,
                          "text": "Up to 25%"
                      }, {
                          "value": 10,
                          "text": "Up to 5%"
                      }
                    ]
                }, {
                    "type": "radiogroup",
                    "name": "profolio_decrease",
                    "title": "What would your reaction be if six months after placing your investment you discover that your portfolio had decreased in value by 20%?",
                    //"isRequired": true,
                    "choices": [
                      {
                          "value": 1,
                          "text": "I would invest more funds to lower my average investment price, expecting future growth"
                      }, {
                          "value": 3,
                          "text": "This was a calculated risk and I would leave the investment in place, expecting future growth"
                      }, {
                          "value": 5,
                          "text": "I would cut my losses"
                      }
                    ]
                }
            ]
        }, {
            "name": "page4",
            "elements": [
                {
                    "type": "radiogroup",
                    "name": "capital_preservation",
                    "title": "To what extent are you concerned about preservation of your capital?",
                    //"isRequired": true,
                    "choices": [
                      {
                          "value": 1,
                          "text": "A high degree of risk would be acceptable given longer term capital growth objectives"
                      }, {
                          "value": 5,
                          "text": "A moderate degree of risk would be acceptable given the potential for increased returns"
                      }, {
                          "value": 10,
                          "text": "A minimal degree of risk would be acceptable for a slight increase in potential returns"
                      }
                    ]
                }, {
                    "type": "radiogroup",
                    "name": "income_requirements",
                    //"visibleIf": "{supported_devices} contains \"Mobile\"",
                    "title": "What are your current income requirements from your investments?",
                    //"isRequired": true,
                    "choices": [
                        {
                            "value": 1,
                            "text": "I require a small amount of investment income as I am mainly focused on capital growth"
                        }, {
                            "value": 3,
                            "text": "I require an equal combination of investment income and capital growth"
                        }, {
                            "value": 5,
                            "text": "I require substantial investment income with only some capital growth"
                        }
                    ]
                }
            ]
        }
    ],
    "completedHtml": "<p><h4>Thank you for sharing this information with us.</h4></p><p>Your total score is: <b id='score'>"+total_score+"</b></p>"+
    "<p>Based on the score from the questions you have answered in the previous section of this questionnaire, you have been determined to be the following type of investor</p>"+
    "<table id="+'risk_tolerance_table'+" align="+'center'+"><thead><th>Score</th><th>Description</th></thead>"+
    "<tbody><tr><td>30 points or less</td><td align="+'left'+"><b>Aggressive:</b><br/><br/>"+
    "An Aggressive Investor is prepared to accept higher risks in order to obtain greater<br/>"+
    "investment returns with a potential to lose all or more of his capital. An Aggressive<br/>"+
    "Investor is comfortable with investments that are more volatile and bear a higher risk<br/>"+
    "of loss of capital. An Aggressive Investor has a high appetite for speculative trading.<br/>"+
    "</td></tr><tr><td>31 - 47 points</td><td align="+'left'+"><b>Balanced:</b><br/><br/>"+
    "A Balanced Investor seeks a mixture of capital growth and regular income from his<br/>"+
    "investments. A Balanced Investor is therefore prepared to accept moderate amounts<br/>"+
    "of risk to earn moderate potential returns. A Balanced Investor accepts that there<br/>"+
    "is a real potential to lose at least part of his capital in seeking moderate returns. A<br/>"+
    "Balanced Investor appreciates that there will be, even in times of stability, occasional<br/>"+
    "periods of volatility and risk of loss of capital. A Balanced Investor may engage in<br/>"+
    "speculative trading from time to time and particularly accepts that when times are<br/>"+
    "uncertain, trading is more likely to be regarded as more inherently speculative.<br/>"+
    "</td></tr><tr><td>48 points or more</td><td align="+'left'+"><b>Conservative:</b><br/><br/>"+
    "You are a Conservative Investor. You seek capital preservation and a safe regular<br/>"+
    "income is a priority over capital growth. You should seriously consider whether you<br/>"+
    "should be investing other than in fixed deposit.<br/><br/>"+
    "A Conservative Investor seeks primarily capital preservation. A Conservative Investor<br/>"+
    "seeks principally a safe and regular income as a priority over capital growth. A<br/>"+
    "Conservative Investor should seriously consider whether he should be putting his<br/>"+
    "money in investments other than in fixed deposit. A Conservative Investor will not<br/>"+
    "be allowed to trade Specified Investment Products ("+"SIPs"+")* with us as there are<br/>"+
    "currently no SIPs which bear little or no risk of capital loss</td></tr></tbody></table><br/>"
    
};

window.survey = new Survey.Model(json);

survey.onComplete.add(function (result, total_score) {
        total_score = result.data.investment_objectives+result.data.risk_capital_percentage+result.data.saving_duration+result.data.inflation_effects+result.data.emergencies_saving+result.data.asset_mixes+result.data.expected_return+result.data.investment_fluctuation+result.data.profolio_decrease+result.data.capital_preservation+result.data.income_requirements;
        document.querySelector('#score').textContent = total_score.toString();
        document.querySelector('#surveyResult').innerHTML = "<form class='form-group' method='POST' action='services/submit_score'><h4>Click Submit to auto-assign to our AUM that fits your Risk Tolerance!<input name='score' value='"+total_score+"' type='hidden' /><button type='submit' class='btn btn-primary mb-2'>Submit Score</button></h4></form>"
        return total_score;
    });
    

$("#surveyElement").Survey({model: survey});

/*
survey
    .onComplete
    .add(function () {
        var surveyResultNode = document.getElementById("surveyResult");
        surveyResultNode.innerHTML = "";

        $.get("/api/MySurveys/getSurveyNPCResults/", function (data) {
            var normalizedData = data
                .Data
                .map(function (item) {
                    survey
                        .getAllQuestions()
                        .forEach(function (q) {
                            if (item[q.name] === undefined) {
                                item[q.name] = "";
                            }
                        });
                    return item;
                });

            var visPanel = new SurveyAnalytics.VisualizationPanel(surveyResultNode, survey.getAllQuestions(), normalizedData);
            visPanel.render();
        });
    });
*/