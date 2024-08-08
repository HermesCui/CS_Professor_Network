async function fetchData() {
    const response = await fetch('network_data.json?' + new Date().getTime()); // Add timestamp to URL to prevent caching
    const data = await response.json();
    return data;
}

function initializeCytoscape(data) {
    const cy = cytoscape({
        container: document.getElementById('cy'),
        elements: data,
        style: [
            {
                selector: 'node',
                style: {
                    'label': 'data(label)',
                    'background-color': 'skyblue',
                    'font-size': '12px',
                    'text-valign': 'center',
                    'color': '#000',
                    'text-outline-width': 1,
                    'text-outline-color': '#fff'
                }
            },
            {
                selector: 'edge',
                style: {
                    'width': 'data(weight)',
                    'line-color': '#ccc',
                    'target-arrow-color': '#ccc',
                    'target-arrow-shape': 'triangle',
                    'curve-style': 'bezier'
                }
            },
            {
                selector: 'node.major',
                style: {
                    'background-color': 'red'
                }
            },
            {
                selector: 'node.secondary',
                style: {
                    'background-color': 'gold'
                }
            },
            {
                selector: 'node.tertiary',
                style: {
                    'background-color': 'pink'
                }
            }
        ],
        layout: {
            name: 'cose',
            padding: 10,
            animate: false, // Disable animation for accurate timing
            fit: true,
            randomize: true,
            nodeRepulsion: 400000,
            idealEdgeLength: 100,
            edgeElasticity: 100,
            gravity: 80,
            numIter: 1000,
            initialTemp: 200,
            coolingFactor: 0.95,
            minTemp: 1.0
        }
    });
   
    cy.nodes().forEach(node => {
        if (majorProfessors.includes(node.id())) {
            node.addClass('major');
            const neighbors = node.neighborhood().nodes();
            neighbors.forEach((neighbor, index) => {
                if (index === 0) neighbor.addClass('major');
                else if (index === 1) neighbor.addClass('secondary');
                else if (index === 2) neighbor.addClass('tertiary');
            });
        }
    });

    return cy;
}

document.getElementById('reload').addEventListener('click', () => {
    fetchData().then(data => {
        initializeCytoscape(data);
    });
});

// Load the data initially
fetchData().then(data => {
    initializeCytoscape(data);
});








