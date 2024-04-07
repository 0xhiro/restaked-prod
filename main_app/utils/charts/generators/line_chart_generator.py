def generate_line_chart_data(x, y):
    """
    Generates the data structure for a Chart.js chart.
    
    :param block_numbers: A list of block numbers for the X-axis.
    :param num_pods: A list of pod counts corresponding to each block number for the Y-axis.
    :return: A dict containing the structured data for the chart.
    """
    chart_data = {
        'type': 'line',
        'data': {
            'labels': x,
            'datasets': [{
                'label': '',
                'data': y,
                'borderColor': 'rgb(75, 192, 192)',
                'tension': 0.1,
                'fill': False,
            }]
        },
        'options': {
            'scales': {
                'y': {
                    'beginAtZero': True,
                    'title': {
                        'display': True,
                        'text': 'Dates'
                    }
                },
                'x': {
                    'title': {
                        'display': True,
                        'text': 'TVL (USD)'
                    }
                }
            },
            'responsive': True,
            'maintainAspectRatio': False,
        }
    }
    
    return chart_data
