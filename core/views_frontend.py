from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index(request):
    html_content = r'''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Таблица маршрутов</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/vue@2/dist/vue.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
    <style>
    .table {
        width: 100%;
    }
    .table th, .table td {
        text-align: center;
        vertical-align: middle;
    }
    .table td:nth-child(4) {
        white-space: nowrap;
    }
</style>
    .table td:last-child, .table th:last-child {
        display: none !important;
    }
<body>
<div id="app" class="container mt-4">
    <h1>📊 Таблица маршрутов</h1>

    <div class="row mb-3 g-2 align-items-end">
        <div class="col-md-3">
            <label class="form-label">Колонка</label>
            <select class="form-select" v-model="filterColumn">
                <option value="name">Название</option>
                <option value="quantity">Количество</option>
                <option value="distance">Расстояние</option>
            </select>
        </div>
        <div class="col-md-3">
            <label class="form-label">Условие</label>
            <select class="form-select" v-model="filterOperator">
                <option v-for="op in operatorsForColumn" :value="op.value">{{ op.text }}</option>
            </select>
        </div>
        <div class="col-md-3">
            <label class="form-label">Значение</label>
            <input type="text" class="form-control" v-model="filterValue" @keyup.enter="applyFilter">
        </div>
        <div class="col-md-2">
            <button class="btn btn-primary w-100" @click="applyFilter">Применить</button>
        </div>
        <div class="col-md-1">
            <button class="btn btn-secondary w-100" @click="clearFilters">Сбросить</button>
        </div>
    </div>

    <table class="table table-bordered">
        <thead>
            <tr>
                <th>Дата</th>
                <th @click="sortBy('name')" style="cursor:pointer">Название ⬍</th>
                <th @click="sortBy('quantity')" style="cursor:pointer">Количество ⬍</th>
                <th @click="sortBy('distance')" style="cursor:pointer">Расстояние ⬍</th>
            </tr>
        </thead>
        <tbody>
    <tr v-for="item in items" :key="item.id">
        <td>{{ item.date }}</td>
        <td>{{ item.name }}</td>
        <td>{{ item.quantity }}</td>
        <td>{{ Number(item.distance).toFixed(2) }}</td>
    </tr>
    <tr v-if="items.length === 0">
        <td colspan="4" class="text-center">Нет данных</td>
    </tr>
</tbody>
    </table>

    <nav>
        <ul class="pagination">
            <li class="page-item" :class="{disabled: currentPage === 1}">
                <a class="page-link" href="#" @click.prevent="changePage(currentPage-1)">Назад</a>
            </li>
            <li class="page-item"><span class="page-link">Страница {{ currentPage }} из {{ totalPages }}</span></li>
            <li class="page-item" :class="{disabled: currentPage === totalPages}">
                <a class="page-link" href="#" @click.prevent="changePage(currentPage+1)">Вперед</a>
            </li>
        </ul>
    </nav>
</div>

<script>
new Vue({
    el: '#app',
    data: {
        items: [],
        currentPage: 1,
        totalPages: 1,
        totalItems: 0,
        sortByField: '',
        sortOrder: 'asc',
        filterColumn: 'name',
        filterOperator: 'contains',
        filterValue: '',
        operatorsMap: {
            name: [
                { value: 'contains', text: 'содержит' },
                { value: 'exact', text: 'равно' }
            ],
            quantity: [
                { value: 'exact', text: 'равно' },
                { value: 'gt', text: 'больше' },
                { value: 'lt', text: 'меньше' }
            ],
            distance: [
                { value: 'exact', text: 'равно' },
                { value: 'gt', text: 'больше' },
                { value: 'lt', text: 'меньше' }
            ]
        }
    },
    computed: {
        operatorsForColumn() {
            return this.operatorsMap[this.filterColumn] || [];
        }
    },
    watch: {
        filterColumn() {
            const ops = this.operatorsForColumn;
            if (ops.length) this.filterOperator = ops[0].value;
            this.applyFilter();
        },
        filterOperator() {
            this.applyFilter();
        }
    },
    mounted() {
        this.loadData();
    },
    methods: {
        loadData() {
            let params = { page: this.currentPage };

            if (this.sortByField) {
                params.ordering = this.sortOrder === 'asc' ? this.sortByField : `-${this.sortByField}`;
            }

            if (this.filterValue && this.filterValue.trim() !== '') {
                const key = `${this.filterColumn}_${this.filterOperator}`;
                params[key] = this.filterValue.trim();
            }

            const url = `/api/items/?${new URLSearchParams(params).toString()}`;
            axios.get(url)
                .then(response => {
                    this.items = response.data.results;
                    this.totalItems = response.data.count;
                    this.totalPages = Math.ceil(this.totalItems / 10);
                })
                .catch(error => {
                    console.error('Ошибка:', error);
                    alert('Ошибка загрузки: ' + (error.response?.data?.detail || error.message));
                });
        },
        sortBy(field) {
            if (this.sortByField === field) {
                this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc';
            } else {
                this.sortByField = field;
                this.sortOrder = 'asc';
            }
            this.currentPage = 1;
            this.loadData();
        },
        applyFilter() {
            this.currentPage = 1;
            this.loadData();
        },
        clearFilters() {
            this.filterColumn = 'name';
            this.filterOperator = 'contains';
            this.filterValue = '';
            this.currentPage = 1;
            this.loadData();
        },
        changePage(page) {
            if (page < 1 || page > this.totalPages) return;
            this.currentPage = page;
            this.loadData();
        }
    }
});
</script>
</body>
</html>'''
    return HttpResponse(html_content)