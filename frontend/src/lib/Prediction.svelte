<script lang="ts">
    import { onMount } from 'svelte';
    import * as d3 from 'd3'; 
    import { predictionStore } from '../utils/predictionStore';

    export let visibility: string = 'hidden';
    let predictionData: any = null;

    const savedPredictionData = localStorage.getItem('predictionData');
    if (savedPredictionData) {
        predictionData = JSON.parse(savedPredictionData);
    }

    predictionStore.subscribe(value => {
        predictionData = value;

        if (predictionData) {
            localStorage.setItem('predictionData', JSON.stringify(predictionData));
            drawChart();
        }
    });

    onMount(() => {
        if (predictionData) {
            drawChart();
        }
    });

    function drawChart() {
    const data = Object.entries(predictionData).map(([label, value]) => ({
        label,
        value: parseFloat(value as string),
    }));

    const width = 640;
    const height = 480;
    const margin = { top: 20, right: 30, bottom: 40, left: 90 };

    d3.select('#bar-chart').selectAll('*').remove();

    const svg = d3.select('#bar-chart')
        .attr('width', width)
        .attr('height', height)
        .append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    const x = d3.scaleLinear()
        .domain([0, d3.max(data, (d: { value: any; }) => d.value) as number])
        .range([0, width - margin.left - margin.right]);

    const y = d3.scaleBand()
        .domain(data.map(d => d.label))
        .range([0, height - margin.top - margin.bottom])
        .padding(0.1);

    svg.append('g')
        .selectAll('rect')
        .data(data)
        .enter()
        .append('rect')
        .attr('x', 0)
        .attr('y', (d: { label: any; }) => y(d.label)!)
        .attr('width', (d: { value: any; }) => x(d.value))
        .attr('height', y.bandwidth())
        .attr('fill', '#FF6961');

    svg.append('g')
        .call(d3.axisLeft(y).tickSize(0))
        .selectAll('text')
        .style('font-size', '14px') 
        .style('font-weight', 'bold')
        .attr('transform', 'translate(-10,0)');

    svg.append('g')
        .attr('transform', `translate(0,${height - margin.top - margin.bottom})`)
        .call(d3.axisBottom(x).ticks(5));

    svg.selectAll('.text')
        .data(data)
        .enter()
        .append('text')
        .attr('class', 'label')
        .attr('x', (d: { value: any; }) => {
            const barWidth = x(d.value);
            const textPadding = 5;

            if (barWidth < 50) {
                return barWidth + textPadding;  
            } else {
                return barWidth - textPadding; 
            }
        })
        .attr('y', (d: { label: any; }) => y(d.label)! + y.bandwidth() / 2)
        .attr('dy', '.35em')
        .attr('text-anchor', (d: { value: any; }) => x(d.value) < 50 ? 'start' : 'end') 
        .style('font-weight', 'bold')
        .attr('fill', 'white')  
        .text((d: { value: number; }) => `${d.value.toFixed(1)}%`);
}
</script>

<style>
    .vertical-line {
        position: absolute;
        top: 0;
        bottom: 0;
        left: 50%;
        width: 1px;
        background-color: rgb(53, 52, 52); 
        transform: translateX(-50%);
        opacity: 0;
        transition: opacity 0.9s ease-in-out;
    }
    
    .visible {
        opacity: 1;
    }

    .bar-chart-container {
        position: absolute;
        right: 9.5%; 
        top: 13%; 
        display: flex;
        flex-direction: column; 
        align-items: flex-end;
        margin-top: 2rem; 
        transition: transform 0.3s ease;
    }
</style>

<div class="vertical-line {visibility === 'visible' ? 'visible' : ''}" style="visibility: {visibility};"></div>

<div class="bar-chart-container {visibility === 'visible' ? 'visible' : ''}" style="visibility: {visibility};">
    <svg id="bar-chart"></svg>
</div>