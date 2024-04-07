def generate_multi_line_chart_data(strategies):
    """
    Generates the data structure for a Chart.js chart with multiple lines, one for each strategy,
    each with a unique color.
    
    :param strategies: A list of Strategy instances, where each Strategy represents a strategy with a name,
                       a list of dates, and a list of share values.
    :return: A dict containing the structured data for the chart.
    """
    # Define a list of colors for the lines
    colors = [
        'rgb(255, 99, 132)',  # Red
        'rgb(54, 162, 235)',  # Blue
        'rgb(255, 206, 86)',  # Yellow
        'rgb(75, 192, 192)',  # Green
        'rgb(153, 102, 255)',  # Purple
        'rgb(255, 159, 64)',  # Orange
        # Add more colors as needed
    ]
    
    # Ensure that there are strategies to process
    if not strategies:
        return {}
    
    # Use the dates from the first strategy for the x-axis labels
    x_axis_labels = strategies[0].dates_list

    datasets = []
    for index, strategy in enumerate(strategies):
        # Select a color for the current strategy
        color = colors[index % len(colors)]  # Cycle through colors if there are more strategies than colors

        # Ensure each strategy has the same length of dates and shares
        if len(strategy.dates_list) != len(strategy.shares_list):
            continue  # or handle error more gracefully

        # Creating a dataset for each strategy
        dataset = {
            'label': strategy.strategy_name,
            'data': strategy.shares_list,
            'borderColor': color,  # Use the selected color
            'tension': 0.1,
            'fill': False,
        }
        datasets.append(dataset)

    # Structuring the data for Chart.js
    chart_data = {
        'type': 'line',
        'data': {
            'labels': x_axis_labels,
            'datasets': datasets
        },
        'options': {
            'scales': {
                'y': {
                    'beginAtZero': True,
                    'title': {
                        'display': True,
                        'text': 'Shares'
                    }
                },
                'x': {
                    'title': {
                        'display': True,
                        'text': 'Date'
                    }
                }
            },
            'responsive': True,
            'maintainAspectRatio': False,
        }
    }
    
    return chart_data

