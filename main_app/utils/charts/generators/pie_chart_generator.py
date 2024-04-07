def generate_pie_chart_data(labels, data):
    """
    Generates the data structure for a Chart.js pie chart with standardized colors.
    
    :param labels: A list of labels for the pie chart.
    :param data: A list of data points corresponding to each label.
    :return: A dict containing the structured data for the chart.
    """
    backgroundColors = [
        'rgba(255, 206, 86, 0.2)',
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(153, 102, 255, 0.2)',
        'rgba(255, 159, 64, 0.2)',
        'rgba(199, 199, 199, 0.2)',
        'rgba(83, 102, 255, 0.2)',
        'rgba(40, 159, 64, 0.2)',
        'rgba(255, 99, 132, 0.2)'  # This list can be extended as needed
    ]
    
    borderColors = [
        'rgba(255, 206, 86, 1)',
        'rgba(255, 99, 132, 1)',
        'rgba(54, 162, 235, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)',
        'rgba(255, 159, 64, 1)',
        'rgba(199, 199, 199, 1)',
        'rgba(83, 102, 255, 1)',
        'rgba(40, 159, 64, 1)',
        'rgba(255, 99, 132, 1)'  # This list can be extended as needed
    ]
    
    chart_data = {
        'type': 'pie',
        'data': {
            'labels': labels,
            'datasets': [{
                'data': data,
                'backgroundColor': backgroundColors,
                'borderColor': borderColors,
                'borderWidth': 1
            }]
        },
        'options': {
            'responsive': True,
            'maintainAspectRatio': False,
        }
    }
    
    return chart_data
