async function fetchCars() {
    try {
        const response = await fetch('https://jurand.pythonanywhere.com/cars');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const cars = await response.json();

        const table = document.getElementById('cars-table-body');
        table.innerHTML = ''; // Clear previous content

        cars.forEach(car => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${car.id}</td>
                <td>${car.make}</td>
                <td>${car.model}</td>
                <td>${car.year}</td>
                <td>${car.vin}</td>
                <td>${car.desc}</td>
            `;
            table.appendChild(row);
        });
    } catch (error) {
        console.error('Error fetching cars:', error);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('cars-link').addEventListener('click', fetchCars);
});