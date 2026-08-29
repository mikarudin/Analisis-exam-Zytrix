import json

# Data rekod (contoh/pemboleh ubah all_records)
all_records = [] 

# Build an interactive single-file HTML Dashboard
html_content = f"""<!DOCTYPE html>
<html lang="ms">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Analisis Prestasi Akademik - SM Sains Kota Tinggi</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        .class-badge-delima {{ background-color: #EBF8FF; color: #2B6CB0; border: 1px solid #90CDF4; }}
        .class-badge-intan {{ background-color: #F0FFF4; color: #276749; border: 1px solid #9AE6B4; }}
        .class-badge-baiduri {{ background-color: #FFFAF0; color: #C05621; border: 1px solid #FBD38D; }}
        .class-badge-nilam {{ background-color: #FAF5FF; color: #6B46C1; border: 1px solid #D6BCFA; }}
        .class-badge-mutiara {{ background-color: #FFF5F5; color: #C53030; border: 1px solid #FEB2B2; }}
    </style>
</head>
<body class="bg-slate-50 text-slate-800 font-sans min-h-screen">

    <!-- Header Banner -->
    <header class="bg-indigo-900 text-white shadow-lg">
        <div class="max-w-7xl mx-auto px-6 py-6 flex flex-col md:flex-row justify-between items-center">
            <div>
                <h1 class="text-2xl font-bold tracking-wide">SM SAINS KOTA TINGGI</h1>
                <p class="text-indigo-200 text-sm mt-1">Dashboard Interaktif Analisis Prestasi Academic (2024 - 2025)</p>
            </div>
            <div class="mt-4 md:mt-0 bg-indigo-800 px-4 py-2 rounded-lg border border-indigo-700 text-right">
                <span class="text-xs text-indigo-300 block">Jumlah Rekod Murid</span>
                <span class="text-xl font-bold text-amber-400">734 Rekod</span>
            </div>
        </div>
    </header>

    <!-- Navigation / Filters -->
    <main class="max-w-7xl mx-auto px-6 py-8">
        
        <div class="bg-white p-6 rounded-xl shadow-sm border border-slate-200 mb-8">
            <h2 class="text-lg font-semibold text-slate-700 mb-4 flex items-center gap-2">
                <svg class="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2a1 1 0 01-.293.707L15 13.586V19a1 1 0 01-.553.894l-4 2A1 1 0 019 21v-7.414L3.293 6.707A1 1 0 013 6V4z"></path></svg>
                Penapis Data Interaktif
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                    <label class="block text-xs font-medium text-slate-500 mb-1">Sesi / Peperiksaan</label>
                    <select id="examFilter" onchange="updateDashboard()" class="w-full bg-slate-50 border border-slate-300 text-slate-800 text-sm rounded-lg p-2.5 focus:ring-indigo-500 focus:border-indigo-500">
                        <option value="UPSA 2025 (T2)" selected>UPSA 2025 (Tingkatan 2)</option>
                        <option value="PDA 1 2025 (T2)">PDA 1 2025 (Tingkatan 2)</option>
                        <option value="UASA 2024/2025 (T1)">UASA 2024/2025 (Tingkatan 1)</option>
                        <option value="PDA 2 2024 (T1)">PDA 2 2024 (Tingkatan 1)</option>
                        <option value="UPSA Nilai 2024 (T1)">UPSA Nilai 2024 (Tingkatan 1)</option>
                    </select>
                </div>
                <div>
                    <label class="block text-xs font-medium text-slate-500 mb-1">Pilih Kelas</label>
                    <select id="classFilter" onchange="updateDashboard()" class="w-full bg-slate-50 border border-slate-300 text-slate-800 text-sm rounded-lg p-2.5 focus:ring-indigo-500 focus:border-indigo-500">
                        <option value="ALL">Semua Kelas</option>
                        <option value="2 DELIMA">2 DELIMA (🔵 Biru)</option>
                        <option value="2 INTAN">2 INTAN (🟢 Hijau)</option>
                        <option value="2 BAIDURI">2 BAIDURI (Jingga)</option>
                        <option value="2 NILAM">2 NILAM (Ungu)</option>
                        <option value="2 MUTIARA">2 MUTIARA (🔴 Merah)</option>
                    </select>
                </div>
                <div>
                    <label class="block text-xs font-medium text-slate-500 mb-1">Cari Murid</label>
                    <input type="text" id="searchInput" onkeyup="updateTableOnly()" placeholder="Taip nama murid..." class="w-full bg-slate-50 border border-slate-300 text-slate-800 text-sm rounded-lg p-2.5 focus:ring-indigo-500 focus:border-indigo-500">
                </div>
            </div>
        </div>

        <!-- Metric KPI Cards -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <div class="bg-white p-5 rounded-xl shadow-sm border border-slate-200">
                <span class="text-xs text-slate-500 font-medium">Bilangan Murid</span>
                <p id="kpiCount" class="text-3xl font-bold text-slate-800 mt-2">0</p>
                <span class="text-xs text-emerald-600 mt-1 inline-block">Calon terdaftar</span>
            </div>
            <div class="bg-white p-5 rounded-xl shadow-sm border border-slate-200">
                <span class="text-xs text-slate-500 font-medium">Purata Peratus</span>
                <p id="kpiAvgPct" class="text-3xl font-bold text-indigo-600 mt-2">0%</p>
                <span class="text-xs text-slate-400 mt-1 inline-block">Keseluruhan subjek</span>
            </div>
            <div class="bg-white p-5 rounded-xl shadow-sm border border-slate-200">
                <span class="text-xs text-slate-500 font-medium">Purata GPK</span>
                <p id="kpiAvgGPK" class="text-3xl font-bold text-amber-500 mt-2">0.00</p>
                <span class="text-xs text-slate-400 mt-1 inline-block">Gred Purata Kertas</span>
            </div>
            <div class="bg-white p-5 rounded-xl shadow-sm border border-slate-200">
                <span class="text-xs text-slate-500 font-medium">Jumlah Gred A</span>
                <p id="kpiCountA" class="text-3xl font-bold text-emerald-600 mt-2">0</p>
                <span class="text-xs text-emerald-600 mt-1 inline-block">Gred Cemerlang</span>
            </div>
        </div>

        <!-- Visual Charts Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
            <div class="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
                <h3 class="text-md font-bold text-slate-700 mb-4">Purata Peratus Markah Mengikut Kelas</h3>
                <div class="relative h-64">
                    <canvas id="classChart"></canvas>
                </div>
            </div>
            <div class="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
                <h3 class="text-md font-bold text-slate-700 mb-4">Taburan Gred Keseluruhan</h3>
                <div class="relative h-64">
                    <canvas id="gredChart"></canvas>
                </div>
            </div>
        </div>

        <!-- Detailed Individual Student Table -->
        <div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden mb-8">
            <div class="p-6 border-b border-slate-200 flex justify-between items-center">
                <h3 class="text-lg font-bold text-slate-800">Senarai Markah & Analisis Individu Murid</h3>
                <span id="recordSummary" class="text-xs text-slate-500">Menunjukkan 0 rekod</span>
            </div>
            <div class="overflow-x-auto">
                <table class="w-full text-sm text-left text-slate-600">
                    <thead class="text-xs text-slate-700 uppercase bg-slate-100 border-b border-slate-200">
                        <tr>
                            <th class="px-4 py-3">Ked</th>
                            <th class="px-4 py-3">Nama Murid</th>
                            <th class="px-4 py-3">Kelas</th>
                            <th class="px-4 py-3 text-center">Peratus (%)</th>
                            <th class="px-4 py-3 text-center">GPK</th>
                            <th class="px-4 py-3 text-center">Gred (A-F)</th>
                            <th class="px-4 py-3">Keputusan</th>
                        </tr>
                    </thead>
                    <tbody id="studentTableBody">
                        <!-- Dynamic Rows -->
                    </tbody>
                </table>
            </div>
        </div>

    </main>

    <script>
        const rawData = {json.dumps(all_records)};

        let classChartInstance = null;
        let gredChartInstance = null;

        function getClassColorClass(kelas) {{
            if (kelas.includes('DELIMA')) return 'class-badge-delima';
            if (kelas.includes('INTAN')) return 'class-badge-intan';
            if (kelas.includes('BAIDURI')) return 'class-badge-baiduri';
            if (kelas.includes('NILAM')) return 'class-badge-nilam';
            if (kelas.includes('MUTIARA')) return 'class-badge-mutiara';
            return 'bg-slate-100 text-slate-700';
        }}

        function getFilteredData() {{
            const selectedExam = document.getElementById('examFilter').value;
            const selectedClass = document.getElementById('classFilter').value;
            
            return rawData.filter(d => {{
                const matchExam = d.Peperiksaan === selectedExam;
                const matchClass = (selectedClass === 'ALL') || (d.Kelas === selectedClass);
                return matchExam && matchClass;
            }});
        }}

        function updateDashboard() {{
            const filtered = getFilteredData();
            
            // KPI Calculations
            const count = filtered.length;
            const avgPct = count > 0 ? (filtered.reduce((acc, c) => acc + c.Peratus, 0) / count).toFixed(2) : '0.00';
            const avgGPK = count > 0 ? (filtered.reduce((acc, c) => acc + c.GPK, 0) / count).toFixed(2) : '0.00';
            const totalA = filtered.reduce((acc, c) => acc + c.A, 0);

            document.getElementById('kpiCount').innerText = count;
            document.getElementById('kpiAvgPct').innerText = avgPct + '%';
            document.getElementById('kpiAvgGPK').innerText = avgGPK;
            document.getElementById('kpiCountA').innerText = totalA;

            updateCharts(filtered);
            updateTableOnly();
        }}

        function updateCharts(filtered) {{
            const classes = ['2 DELIMA', '2 INTAN', '2 BAIDURI', '2 NILAM', '2 MUTIARA', '1 DELIMA', '1 INTAN', '1 BAIDURI', '1 NILAM', '1 MUTIARA'];
            const classAverages = {{}};
            
            filtered.forEach(d => {{
                if (!classAverages[d.Kelas]) classAverages[d.Kelas] = {{ sum: 0, count: 0 }};
                classAverages[d.Kelas].sum += d.Peratus;
                classAverages[d.Kelas].count += 1;
            }});

            const labels = Object.keys(classAverages);
            const dataAvg = labels.map(k => (classAverages[k].sum / classAverages[k].count).toFixed(2));

            if (classChartInstance) classChartInstance.destroy();
            const ctxClass = document.getElementById('classChart').getContext('2d');
            classChartInstance = new Chart(ctxClass, {{
                type: 'bar',
                data: {{
                    labels: labels,
                    datasets: [{{
                        label: 'Purata Peratus (%)',
                        data: dataAvg,
                        backgroundColor: ['#3182CE', '#38A169', '#DD6B20', '#805AD5', '#E53E3E']
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{ y: {{ min: 0, max: 100 }} }}
                }}
            }});

            const totalA = filtered.reduce((acc, c) => acc + c.A, 0);
            const totalB = filtered.reduce((acc, c) => acc + c.B, 0);
            const totalC = filtered.reduce((acc, c) => acc + c.C, 0);
            const totalD = filtered.reduce((acc, c) => acc + c.D, 0);
            const totalE = filtered.reduce((acc, c) => acc + c.E, 0);
            const totalF = filtered.reduce((acc, c) => acc + c.F, 0);

            if (gredChartInstance) gredChartInstance.destroy();
            const ctxGred = document.getElementById('gredChart').getContext('2d');
            gredChartInstance = new Chart(ctxGred, {{
                type: 'doughnut',
                data: {{
                    labels: ['A', 'B', 'C', 'D', 'E', 'F'],
                    datasets: [{{
                        data: [totalA, totalB, totalC, totalD, totalE, totalF],
                        backgroundColor: ['#22c55e', '#3b82f6', '#f59e0b', '#f97316', '#ef4444', '#64748b']
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false
                }}
            }});
        }}

        function updateTableOnly() {{
            const filtered = getFilteredData();
            const searchKeyword = document.getElementById('searchInput').value.toLowerCase();
            
            const tableBody = document.getElementById('studentTableBody');
            tableBody.innerHTML = '';

            const searched = filtered.filter(d => d.Nama.toLowerCase().includes(searchKeyword));
            document.getElementById('recordSummary').innerText = `Menunjukkan ${{searched.length}} daripada ${{filtered.length}} rekod`;

            searched.forEach(d => {{
                const badgeClass = getClassColorClass(d.Kelas);
                const row = document.createElement('tr');
                row.className = "border-b border-slate-100 hover:bg-slate-50 transition-colors";
                row.innerHTML = `
                    <td class="px-4 py-3 font-semibold text-slate-700">${{d.Kedudukan}}</td>
                    <td class="px-4 py-3 font-medium text-slate-900">${{d.Nama}}</td>
                    <td class="px-4 py-3"><span class="text-xs px-2.5 py-1 rounded-full font-semibold ${{badgeClass}}">${{d.Kelas}}</span></td>
                    <td class="px-4 py-3 text-center font-bold text-indigo-600">${{d.Peratus}}%</td>
                    <td class="px-4 py-3 text-center font-semibold text-slate-700">${{d.GPK}}</td>
                    <td class="px-4 py-3 text-center text-xs">
                        <span class="text-emerald-600 font-bold">${{d.A}}A</span> 
                        <span class="text-blue-600 font-bold">${{d.B}}B</span> 
                        <span class="text-amber-600 font-bold">${{d.C}}C</span>
                    </td>
                    <td class="px-4 py-3 text-xs font-medium text-slate-600">${{d.Keputusan}}</td>
                `;
                tableBody.appendChild(row);
            }});
        }}

        window.onload = function() {{
            updateDashboard();
        }};
    </script>
</body>
</html>
"""

# Nama fail telah ditukar kepada index.html di sini
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Fail index.html berjaya dicipta!")