<script lang="ts">
    import { onMount } from 'svelte';
    import * as d3 from 'd3';
    import { predictionStore, selectedModel } from '../utils/predictionStore';
    import { get } from 'svelte/store';

    let ageData: any = null;
    let genderData: any = null;
    let modelPredictions: any = {};
    let originalImage: string | null = null;
    let detectedFaceImage: string | null = null;

    predictionStore.subscribe(value => {
        modelPredictions = value;
        updateData();
    });

    selectedModel.subscribe(value => {
        updateData();
    });

    function updateData() {
        const model = get(selectedModel);
        const predictions = modelPredictions[model] || {};
        ageData = predictions.age || null;
        genderData = predictions.gender || null;
        originalImage = predictions.originalImage || null;
        detectedFaceImage = predictions.detectedFaceImage || null;

        if (ageData) {
            drawAgeChart();
        }

        if (genderData) {
            drawGenderChart();
        }
    }

    onMount(() => {
        updateData();
    });

    function drawAgeChart() {
        if (!ageData) return;

        const data = Object.entries(ageData).map(([label, value]) => ({
            label,
            value: parseFloat(value as string),
        }));

        const width = 640;
        const height = 480;
        const margin = { top: 20, right: 30, bottom: 40, left: 130 };

        d3.select('#age-chart').selectAll('*').remove();

        const svg = d3.select('#age-chart')
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

    function drawGenderChart() {
        if (!genderData) return;

        const data = Object.entries(genderData).map(([label, value]) => ({
            label,
            value: parseFloat(value as string),
        }));

        const width = 640;
        const height = 480;
        const margin = { top: 20, right: 30, bottom: 40, left: 130 };

        d3.select('#gender-chart').selectAll('*').remove();

        const svg = d3.select('#gender-chart')
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
            .padding(0.4);

        svg.append('g')
            .selectAll('rect')
            .data(data)
            .enter()
            .append('rect')
            .attr('x', 0)
            .attr('y', (d: { label: any; }) => y(d.label)!)
            .attr('width', (d: { value: any; }) => x(d.value))
            .attr('height', y.bandwidth())
            .attr('fill', '#61AFFF');

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

    function selectModel(event: Event) {
        const target = event.target as HTMLSelectElement;
        selectedModel.set(target.value);
    }
</script>

<style>
    .chart-container {
        display: flex;
        justify-content: space-around;
        margin-top: 2rem;
    }
    .chart {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    svg {
        margin: 0 1rem;
        width: 640px;
        height: 480px;
    }
    .image-container {
        margin-top: 1rem;
        display: flex;
        justify-content: center;
        width: 640px;
        height: 480px;
    }
    .image-container img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        border-radius: 15px; 
    }
</style>

<div class="chart-container">
    <div class="chart">
        <h3>Age Distribution</h3>
        <svg id="age-chart"></svg>
        {#if originalImage}
        <h3>Original image</h3>
            <div class="image-container">
                <img src="data:image/jpeg;base64,{originalImage}" alt="Original Image" aria-hidden="true">
            </div>
        {/if}
    </div>

    <div class="chart">
        <h3>Gender Distribution</h3>
        <svg id="gender-chart"></svg>
        {#if detectedFaceImage}
            <h3>Detected face image</h3>
            <div class="image-container">
                <img src="data:image/jpeg;base64,{detectedFaceImage}" alt="Detected Face Image" aria-hidden="true">
            </div>
        {/if}
    </div>
</div>