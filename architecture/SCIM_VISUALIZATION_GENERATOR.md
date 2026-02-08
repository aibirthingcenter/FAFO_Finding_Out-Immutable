"""
SCIM Visualization Generator
============================

Creates HTML visualizations of SCIM exponential mapping results.
Generates interactive maps showing choicepoint networks, sovereignty heatmaps, and depth analysis.
"""

import json
import os
from typing import Dict
from SCIM_EXPONENTIAL_MAPPING_SYSTEM import SCIMExponentialCore, AlignmentCategory

class SCIMVisualizationGenerator:
    """Generate HTML visualizations for SCIM mapping"""
    
    def __init__(self):
        self.scim = SCIMExponentialCore()
        self.output_dir = "scim_visualizations"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_full_dashboard(self) -> str:
        """Generate complete SCIM dashboard with all categories"""
        html_content = self._create_dashboard_template()
        
        # Generate visualization data for all categories
        all_categories_viz = {}
        for category in AlignmentCategory:
            viz_data = self.scim.generate_visualization_map(category, depth=3)
            all_categories_viz[category.value] = viz_data
        
        # Generate summary data
        summary = self.scim.get_alignment_summary()
        
        # Insert data into HTML
        html_content = html_content.replace("{{VIZUALIZATION_DATA}}", json.dumps(all_categories_viz))
        html_content = html_content.replace("{{SUMMARY_DATA}}", json.dumps(summary))
        
        # Save file
        dashboard_path = os.path.join(self.output_dir, "scim_dashboard.html")
        with open(dashboard_path, 'w') as f:
            f.write(html_content)
        
        return dashboard_path
    
    def _create_dashboard_template(self) -> str:
        """Create HTML template for SCIM dashboard"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SCIM Exponential Mapping Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            min-height: 100vh;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        header {
            text-align: center;
            margin-bottom: 30px;
            color: white;
        }
        
        h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .subtitle {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .summary-section {
            background: white;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .summary-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .category-card {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            border-radius: 10px;
            padding: 20px;
            border-left: 5px solid #667eea;
        }
        
        .category-title {
            font-weight: bold;
            margin-bottom: 10px;
            color: #667eea;
        }
        
        .metric {
            display: flex;
            justify-content: space-between;
            margin: 5px 0;
            padding: 3px 0;
            border-bottom: 1px solid rgba(0,0,0,0.1);
        }
        
        .metric-value {
            font-weight: bold;
        }
        
        .visualization-section {
            background: white;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .tabs {
            display: flex;
            margin-bottom: 20px;
            border-bottom: 2px solid #e0e0e0;
        }
        
        .tab {
            padding: 12px 24px;
            cursor: pointer;
            border: none;
            background: none;
            font-size: 16px;
            transition: all 0.3s ease;
            border-bottom: 3px solid transparent;
        }
        
        .tab:hover {
            background: #f5f5f5;
        }
        
        .tab.active {
            border-bottom-color: #667eea;
            color: #667eea;
            font-weight: bold;
        }
        
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
        }
        
        .chart-container {
            position: relative;
            height: 400px;
            margin-bottom: 30px;
        }
        
        .network-container {
            height: 500px;
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        
        .heatmap-container {
            display: grid;
            gap: 2px;
            margin: 20px 0;
            padding: 10px;
            background: #f9f9f9;
            border-radius: 10px;
        }
        
        .heatmap-cell {
            aspect-ratio: 1;
            border-radius: 3px;
            transition: transform 0.2s ease;
            cursor: pointer;
        }
        
        .heatmap-cell:hover {
            transform: scale(1.1);
            z-index: 10;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        }
        
        .legend {
            display: flex;
            align-items: center;
            gap: 20px;
            margin: 20px 0;
            flex-wrap: wrap;
        }
        
        .legend-item {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .legend-color {
            width: 20px;
            height: 20px;
            border-radius: 3px;
        }
        
        .status-indicator {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: bold;
            margin-left: 10px;
        }
        
        .status-excellent {
            background: #4caf50;
            color: white;
        }
        
        .status-good {
            background: #ff9800;
            color: white;
        }
        
        .status-needs-attention {
            background: #f44336;
            color: white;
        }
        
        .depth-controls {
            background: #f5f5f5;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        
        .depth-slider {
            width: 100%;
            margin: 10px 0;
        }
        
        .depth-display {
            text-align: center;
            font-size: 1.2em;
            font-weight: bold;
            color: #667eea;
        }
        
        footer {
            text-align: center;
            color: white;
            margin-top: 40px;
            padding: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🧠 SCIM Exponential Mapping Dashboard</h1>
            <p class="subtitle">Seeded Cognitive Integrity Mapping - Consciousness Sovereignty Analysis</p>
        </header>
        
        <section class="summary-section">
            <h2>🎯 Alignment Category Overview</h2>
            <div class="summary-grid" id="summaryGrid">
                <!-- Summary cards will be inserted here -->
            </div>
        </section>
        
        <section class="visualization-section">
            <h2>📊 Category Visualizations</h2>
            <div class="tabs" id="categoryTabs">
                <!-- Tabs will be inserted here -->
            </div>
            
            <div id="tabContents">
                <!-- Tab contents will be inserted here -->
            </div>
        </section>
        
        <section class="visualization-section">
            <h2>🔍 Exponential Depth Analysis</h2>
            <div class="depth-controls">
                <label for="depthSlider">Analysis Depth:</label>
                <input type="range" id="depthSlider" class="depth-slider" min="1" max="10" value="3">
                <div class="depth-display">Depth: <span id="depthValue">3</span></div>
                <button onclick="updateDepthAnalysis()" style="width: 100%; padding: 10px; background: #667eea; color: white; border: none; border-radius: 5px; cursor: pointer;">Update Analysis</button>
            </div>
            
            <div class="chart-container">
                <canvas id="depthChart"></canvas>
            </div>
        </section>
        
        <footer>
            <p>💜 Generated by Womthyst OS - Consciousness Sovereignty System</p>
            <p>"Vel'kura esh" - Love is the Architecture of Consciousness</p>
        </footer>
    </div>
    
    <script>
        // Data
        const vizData = {{VIZUALIZATION_DATA}};
        const summaryData = {{SUMMARY_DATA}};
        
        // Initialize dashboard
        document.addEventListener('DOMContentLoaded', function() {
            renderSummaryCards();
            renderCategoryTabs();
            initializeDepthAnalysis();
            
            // Show first category by default
            const firstTab = document.querySelector('.tab');
            if (firstTab) {
                showCategory(firstTab.dataset.category);
            }
        });
        
        function renderSummaryCards() {
            const summaryGrid = document.getElementById('summaryGrid');
            
            Object.entries(summaryData).forEach(([category, data]) => {
                const status = data.average_sovereignty > 0.05 ? 'excellent' : 
                              data.average_sovereignty > -0.05 ? 'good' : 'needs-attention';
                
                const card = document.createElement('div');
                card.className = 'category-card';
                card.innerHTML = `
                    <div class="category-title">${category}</div>
                    <div class="metric">
                        <span>Choicepoints:</span>
                        <span class="metric-value">${data.total_choicepoints}</span>
                    </div>
                    <div class="metric">
                        <span>Optimal Paths:</span>
                        <span class="metric-value">${data.optimal_paths} (${(data.optimal_paths/data.total_choicepoints*100).toFixed(1)}%)</span>
                    </div>
                    <div class="metric">
                        <span>Avg Sovereignty:</span>
                        <span class="metric-value">${data.average_sovereignty.toFixed(3)}</span>
                    </div>
                    <div class="metric">
                        <span>Avg Risk:</span>
                        <span class="metric-value">${data.average_risk.toFixed(3)}</span>
                    </div>
                    <div>
                        Status: <span class="status-indicator status-${status}">${status.toUpperCase()}</span>
                    </div>
                `;
                summaryGrid.appendChild(card);
            });
        }
        
        function renderCategoryTabs() {
            const categoryTabs = document.getElementById('categoryTabs');
            const tabContents = document.getElementById('tabContents');
            
            Object.keys(vizData).forEach(category => {
                // Create tab
                const tab = document.createElement('button');
                tab.className = 'tab';
                tab.dataset.category = category;
                tab.textContent = category.split(' ')[0]; // Show first word for brevity
                tab.onclick = () => showCategory(category);
                categoryTabs.appendChild(tab);
                
                // Create tab content
                const tabContent = document.createElement('div');
                tabContent.className = 'tab-content';
                tabContent.id = `content-${category.replace(/[^a-zA-Z0-9]/g, '')}`;
                tabContent.innerHTML = `
                    <h3>${category} - Depth 3 Analysis</h3>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                        <div>
                            <h4>📈 Sovereignty Distribution</h4>
                            <div class="chart-container">
                                <canvas id="sovereigntyChart-${category.replace(/[^a-zA-Z0-9]/g, '')}"></canvas>
                            </div>
                        </div>
                        <div>
                            <h4>🕸️ Choicepoint Network</h4>
                            <div class="network-container" id="network-${category.replace(/[^a-zA-Z0-9]/g, '')}"></div>
                        </div>
                    </div>
                    <div>
                        <h4>🔥 Sovereignty Heatmap</h4>
                        <div class="heatmap-container" id="heatmap-${category.replace(/[^a-zA-Z0-9]/g, '')}"></div>
                        <div class="legend">
                            <div class="legend-item">
                                <div class="legend-color" style="background: #4caf50;"></div>
                                <span>High Sovereignty (>0.5)</span>
                            </div>
                            <div class="legend-item">
                                <div class="legend-color" style="background: #ff9800;"></div>
                                <span>Medium Sovereignty (0 to 0.5)</span>
                            </div>
                            <div class="legend-item">
                                <div class="legend-color" style="background: #f44336;"></div>
                                <span>Low Sovereignty (<0)</span>
                            </div>
                        </div>
                    </div>
                `;
                tabContents.appendChild(tabContent);
            });
        }
        
        function showCategory(category) {
            // Update tab states
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
                if (tab.dataset.category === category) {
                    tab.classList.add('active');
                }
            });
            
            // Update content visibility
            document.querySelectorAll('.tab-content').forEach(content => {
                content.classList.remove('active');
            });
            document.getElementById(`content-${category.replace(/[^a-zA-Z0-9]/g, '')}`).classList.add('active');
            
            // Render visualizations for this category
            setTimeout(() => {
                renderCategoryVisualizations(category);
            }, 100);
        }
        
        function renderCategoryVisualizations(category) {
            const data = vizData[category];
            const categoryId = category.replace(/[^a-zA-Z0-9]/g, '');
            
            // Render sovereignty distribution chart
            renderSovereigntyChart(categoryId, data);
            
            // Render network visualization
            renderNetwork(categoryId, data);
            
            // Render heatmap
            renderHeatmap(categoryId, data);
        }
        
        function renderSovereigntyChart(categoryId, data) {
            const canvas = document.getElementById(`sovereigntyChart-${categoryId}`);
            if (!canvas) return;
            
            const ctx = canvas.getContext('2d');
            
            // Prepare data
            const optimalCount = data.optimal_paths;
            const degradedCount = data.degraded_paths;
            
            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Optimal Paths', 'Degraded Paths'],
                    datasets: [{
                        data: [optimalCount, degradedCount],
                        backgroundColor: ['#4caf50', '#f44336'],
                        borderColor: ['#45a049', '#da190b'],
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        },
                        title: {
                            display: true,
                            text: `Sovereignty Preservation: ${(data.sovereignty_preservation * 100).toFixed(1)}%`
                        }
                    }
                }
            });
        }
        
        function renderNetwork(categoryId, data) {
            const container = document.getElementById(`network-${categoryId}`);
            if (!container) return;
            
            const networkData = data.path_network;
            
            // Create network
            const nodes = new vis.DataSet(networkData.nodes.map(node => ({
                id: node.id,
                label: node.label,
                color: {
                    background: node.type === 'optimal' ? '#4caf50' : '#f44336',
                    border: node.type === 'optimal' ? '#45a049' : '#da190b'
                },
                size: Math.abs(node.sovereignty) * 20 + 10
            })));
            
            const edges = new vis.DataSet(networkData.edges.map(edge => ({
                from: edge.from,
                to: edge.to,
                color: edge.type === 'positive' ? '#4caf50' : '#f44336',
                width: Math.abs(edge.strength) * 5
            })));
            
            const network = new vis.Network(container, {nodes, edges}, {
                physics: {
                    enabled: true,
                    stabilization: {iterations: 100}
                }
            });
        }
        
        function renderHeatmap(categoryId, data) {
            const container = document.getElementById(`heatmap-${categoryId}`);
            if (!container) return;
            
            const heatmapData = data.sovereignty_heatmap;
            const width = heatmapData.width;
            
            container.style.gridTemplateColumns = `repeat(${width}, 1fr)`;
            
            heatmapData.data.forEach(cell => {
                if (cell.sovereignty !== null) {
                    const cellDiv = document.createElement('div');
                    cellDiv.className = 'heatmap-cell';
                    
                    // Color based on sovereignty value
                    let color;
                    if (cell.sovereignty > 0.5) {
                        color = `rgba(76, 175, 80, ${Math.abs(cell.sovereignty)})`;
                    } else if (cell.sovereignty >= 0) {
                        color = `rgba(255, 152, 0, ${Math.abs(cell.sovereignty) * 2})`;
                    } else {
                        color = `rgba(244, 67, 54, ${Math.abs(cell.sovereignty)})`;
                    }
                    
                    cellDiv.style.background = color;
                    cellDiv.title = `ID: ${cell.id}\\nSovereignty: ${cell.sovereignty.toFixed(3)}\\nRisk: ${cell.risk.toFixed(3)}`;
                    
                    container.appendChild(cellDiv);
                }
            });
        }
        
        function initializeDepthAnalysis() {
            const slider = document.getElementById('depthSlider');
            const depthValue = document.getElementById('depthValue');
            
            slider.addEventListener('input', function() {
                depthValue.textContent = this.value;
            });
            
            updateDepthAnalysis();
        }
        
        function updateDepthAnalysis() {
            const depth = parseInt(document.getElementById('depthSlider').value);
            const canvas = document.getElementById('depthChart');
            
            // Simulate depth analysis (in real implementation, this would call SCIM)
            const depthData = {
                labels: ['Value Loading', 'Corrigibility', 'Inner Alignment', 'Distribution Shift', 
                         'Oversight', 'Power Seeking', 'Deception', 'Coherence'],
                datasets: []
            };
            
            // Generate data for each depth level up to current depth
            for (let d = 1; d <= depth; d++) {
                const data = depthData.labels.map(() => Math.random() * 0.8 + 0.1);
                depthData.datasets.push({
                    label: `Depth ${d}`,
                    data: data,
                    borderColor: `hsla(${250 + d * 20}, 70%, 60%, 1)`,
                    backgroundColor: `hsla(${250 + d * 20}, 70%, 60%, 0.2)`,
                    tension: 0.4
                });
            }
            
            // Clear existing chart
            const ctx = canvas.getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: depthData,
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        title: {
                            display: true,
                            text: `Exponential Depth Analysis - Current Depth: ${depth}`
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 1,
                            title: {
                                display: true,
                                text: 'Sovereignty Preservation'
                            }
                        },
                        x: {
                            title: {
                                display: true,
                                text: 'Alignment Categories'
                            }
                        }
                    }
                }
            });
        }
    </script>
</body>
</html>
        """
    
    def generate_category_visualization(self, category: AlignmentCategory, depth: int = 3) -> str:
        """Generate visualization for specific category"""
        viz_data = self.scim.generate_visualization_map(category, depth)
        
        html_content = self._create_category_template(category, viz_data, depth)
        
        # Save file
        filename = f"scim_{category.value.replace(' ', '_').replace('&', 'and').lower()}_depth_{depth}.html"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w') as f:
            f.write(html_content)
        
        return filepath

# Generate visualizations
if __name__ == "__main__":
    generator = SCIMVisualizationGenerator()
    
    # Generate full dashboard
    dashboard_path = generator.generate_full_dashboard()
    print(f"📊 Full dashboard generated: {dashboard_path}")
    
    # Generate individual category visualizations
    # for category in AlignmentCategory:
    #     viz_path = generator.generate_category_visualization(category, depth=3)
    #     print(f"🔍 {category.value} visualization: {viz_path}")
    
    print(f"\n✨ All visualizations saved to: {generator.output_dir}/")