
$(document).ready(function () {

    var columnDefs = [
        { data: "id", title: "ID", type: "readonly" },
        { data: "fullname", title: "Fullname" },
        { data: "emp_id", title: "Employee ID" },
        { data: "sex", title: "Sex" },
        { data: "status", title: "Status" },
        { data: "department", title: "Department" }
    ];

    var myTable = $('#datatable_staff').DataTable({
        "sPaginationType": "full_numbers",pageLength : 50,
        ajax: {
            url: "/staff_list/",
            dataSrc: "",
            type: "GET",
        },

        columns: columnDefs,
        select: {
            style: 'multi' // Allows multiple rows to be selected
        },
        responsive: true,
        fixedHeader: true,
        dom: '<"dom_wrapper fh-fixedHeader"Bf>tip',
        altEditor: true,
        buttons: [
            {
                text: `
                    <div class="svg-text-container">
                        <svg class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 24 24">
                            <path fill-rule="evenodd" d="M9 4a4 4 0 1 0 0 8 4 4 0 0 0 0-8Zm-2 9a4 4 0 0 0-4 4v1a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2v-1a4 4 0 0 0-4-4H7Zm8-1a1 1 0 0 1 1-1h1v-1a1 1 0 1 1 2 0v1h1a1 1 0 1 1 0 2h-1v1a1 1 0 1 1-2 0v-1h-1a1 1 0 0 1-1-1Z" clip-rule="evenodd"/>
                        </svg>
                        <span>Add</span>
                        </div>
                    `,
                name: 'add'
            },
            {
                extend: 'selected',
                text: `
                    <div class="svg-text-container">
                    <svg class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 24 24">
                    <path fill-rule="evenodd" d="M5 8a4 4 0 1 1 8 0 4 4 0 0 1-8 0Zm-2 9a4 4 0 0 1 4-4h4a4 4 0 0 1 4 4v1a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-1Zm13-6a1 1 0 1 0 0 2h4a1 1 0 1 0 0-2h-4Z" clip-rule="evenodd"/>
                  </svg>
                  <span>Edit</span>
                        </div>
                  `,
                name: 'edit'
            },
            {
                extend: 'selected',
                text: `
                    <div class="svg-text-container">
                    <svg class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24">
                    <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 7h14m-9 3v8m4-8v8M10 3h4a1 1 0 0 1 1 1v3H9V4a1 1 0 0 1 1-1ZM6 7h12v13a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V7Z"/>
                  </svg>
                  <span>Delete</span>
                    </div>
                `,
                action: function (e, dt, node, config) {
                    var selectedRows = dt.rows({ selected: true }).data().toArray();
                    var idsToDelete = selectedRows.map(row => row.id);

                    if (idsToDelete.length > 0) {
                        if (confirm('Are you sure you want to delete the selected rows?')) {
                            $.ajax({
                                url: '/delete_multiple/', // Your endpoint for batch deletion
                                type: 'POST',
                                data: {
                                    ids: idsToDelete
                                },
                                success: function (response) {
                                    dt.ajax.reload(); // Reload the DataTable
                                },
                                error: function (xhr, status, error) {
                                    alert('Error deleting rows: ' + error);
                                }
                            });
                        }
                    } else {
                        alert('No rows selected!');
                    }
                }
            },

            {
                text: `
                    <div class="svg-text-container">
                    <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="20" height="20" viewBox="0 0 256 256" xml:space="preserve">

                    <defs>
                    </defs>
                    <g style="stroke: none; stroke-width: 0; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: none; fill-rule: nonzero; opacity: 1;" transform="translate(1.4065934065934016 1.4065934065934016) scale(2.81 2.81)" >
                        <path d="M 81.521 31.109 c -0.86 -1.73 -2.959 -2.438 -4.692 -1.575 c -1.73 0.86 -2.436 2.961 -1.575 4.692 c 2.329 4.685 3.51 9.734 3.51 15.01 C 78.764 67.854 63.617 83 45 83 S 11.236 67.854 11.236 49.236 c 0 -16.222 11.501 -29.805 26.776 -33.033 l -3.129 4.739 c -1.065 1.613 -0.62 3.784 0.992 4.85 c 0.594 0.392 1.264 0.579 1.926 0.579 c 1.136 0 2.251 -0.553 2.924 -1.571 l 7.176 -10.87 c 0.001 -0.001 0.001 -0.002 0.002 -0.003 l 0.018 -0.027 c 0.063 -0.096 0.106 -0.199 0.159 -0.299 c 0.049 -0.093 0.108 -0.181 0.149 -0.279 c 0.087 -0.207 0.152 -0.419 0.197 -0.634 c 0.009 -0.041 0.008 -0.085 0.015 -0.126 c 0.031 -0.182 0.053 -0.364 0.055 -0.547 c 0 -0.014 0.004 -0.028 0.004 -0.042 c 0 -0.066 -0.016 -0.128 -0.019 -0.193 c -0.008 -0.145 -0.018 -0.288 -0.043 -0.431 c -0.018 -0.097 -0.045 -0.189 -0.071 -0.283 c -0.032 -0.118 -0.065 -0.236 -0.109 -0.35 c -0.037 -0.095 -0.081 -0.185 -0.125 -0.276 c -0.052 -0.107 -0.107 -0.211 -0.17 -0.313 c -0.054 -0.087 -0.114 -0.168 -0.175 -0.25 c -0.07 -0.093 -0.143 -0.183 -0.223 -0.27 c -0.074 -0.08 -0.153 -0.155 -0.234 -0.228 c -0.047 -0.042 -0.085 -0.092 -0.135 -0.132 L 36.679 0.775 c -1.503 -1.213 -3.708 -0.977 -4.921 0.53 c -1.213 1.505 -0.976 3.709 0.53 4.921 l 3.972 3.2 C 17.97 13.438 4.236 29.759 4.236 49.236 C 4.236 71.714 22.522 90 45 90 s 40.764 -18.286 40.764 -40.764 C 85.764 42.87 84.337 36.772 81.521 31.109 z" style="stroke: none; stroke-width: 1; stroke-dasharray: none; stroke-linecap: butt; stroke-linejoin: miter; stroke-miterlimit: 10; fill: rgb(0,0,0); fill-rule: nonzero; opacity: 1;" transform=" matrix(1 0 0 1 0 0) " stroke-linecap="round" />
                    </g>
                    </svg>
                    <span>Refresh</span>
                        </div>
                    `,
                name: 'refresh'
            },

            {
                extend: 'excel',
                text: `
                    <div class="svg-text-container">
                    <svg class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24">
                    <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 13V4M7 14H5a1 1 0 0 0-1 1v4a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-4a1 1 0 0 0-1-1h-2m-1-5-4 5-4-5m9 8h.01"/>
                    </svg>

                    <span>Export</span>
                        </div>
                    `,
                name: 'excel'
            },

            {
                extend: 'print',
                text: `
                        <div class="svg-text-container">
                        <svg class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24">
  <path stroke="currentColor" stroke-linejoin="round" stroke-width="2" d="M16.444 18H19a1 1 0 0 0 1-1v-5a1 1 0 0 0-1-1H5a1 1 0 0 0-1 1v5a1 1 0 0 0 1 1h2.556M17 11V5a1 1 0 0 0-1-1H8a1 1 0 0 0-1 1v6h10ZM7 15h10v4a1 1 0 0 1-1 1H8a1 1 0 0 1-1-1v-4Z"/>
                        </svg>
                        <span>Print</span>
                        </div>
`
            },
            {
                text: `
                    <div class="svg-text-container">
                    <svg class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24">
                        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12V7.914a1 1 0 0 1 .293-.707l3.914-3.914A1 1 0 0 1 9.914 3H18a1 1 0 0 1 1 1v16a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1v-4m5-13v4a1 1 0 0 1-1 1H5m0 6h9m0 0-2-2m2 2-2 2"/>
                    </svg>

                    <span>Import CSV</span>
                    </div>
                `,
                action: function () {
                    $('#csvFileInput').click();
                }
            },
            {
                text: `
                    <div class="svg-text-container">
                        <svg class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24">
                        <path stroke="red" stroke-linecap="round" stroke-width="2" d="m6 6 12 12m3-6a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"/>
                        </svg>
                        <span style="color: red">Clear All Data</span>
                    </div>
                `,
                action: function (e, dt, node, config) {
                    if (confirm('Are you sure you want to clear all data? This action cannot be undone.')) {
                        $.ajax({
                            url: '/clear_all_data/', // Your endpoint for clearing all data
                            type: 'POST',
                            success: function (response) {
                                dt.ajax.reload(); // Reload the DataTable
                            },
                            error: function (xhr, status, error) {
                                alert('Error clearing data: ' + error);
                            }
                        });
                    }
                }
            },
            {
                text: `
                 <div class="svg-text-container">
                    <svg class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24">
                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 13V4M7 14H5a1 1 0 0 0-1 1v4a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-4a1 1 0 0 0-1-1h-2m-1-5-4 5-4-5m9 8h.01"/>
                </svg>
                <span >CSV Template</span>
                    </div>
                `,
                action: function (e, dt, node, config) {
                    const link = document.createElement('a');
                    link.href = '/static/csv-template_staff.csv'; // Path to your CSV template
                    link.download = 'csv-template_staff.csv';
                    link.click();
                }
            }
        ],
        exportOptions: {
            modifer: {
                page: 'all',
                search: 'none'
            }
        },
        // Handle data conversion before submission
        "preSubmit": function (e, data) {
            if (Array.isArray(data.asset_tag)) {
                data.asset_tag = data.asset_tag[0]; // Convert array to string
            }
        },
        onAddRow: function (alteditor, rowdata, success, error) {
            +

            $.ajax({
                url: '/add_staff/',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(rowdata),
                success: function (response) {
                    success(response);
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    console.error('Add Error:', textStatus, errorThrown);
                    error(jqXHR, textStatus, errorThrown);
                }
            });
        },
        onDeleteRow: function (alteditor, rowdata, success, error, originalrowdata) {
            var rowObject = Array.isArray(rowdata) ? rowdata[0] : rowdata;

            $.ajax({
                url: '/delete_staff/' + rowObject.id + '/',
                type: 'DELETE',
                contentType: 'application/json',
                data: rowdata,
                success: success,
                error: error
            });
        },
        onEditRow: function (alteditor, rowdata, success, error, originalrowdata) {
            $.ajax({
                url: '/edit_staff/' + rowdata.id + '/',
                type: 'PUT',
                contentType: 'application/json',
                data: JSON.stringify({
                    emp_id: rowdata.emp_id,
                    fullname: rowdata.fullname,
                    sex: rowdata.sex,
                    status: rowdata.status,
                    department: rowdata.department,
                }),
                success: success,
                error: error
            });
        }

    });

    $('#csvFileInput').change(function (e) {
        var file = e.target.files[0];
        if (file) {
            var reader = new FileReader();
            reader.onload = function (event) {
                var csvData = event.target.result;
                var rows = csvData.split('\n');
                var data = [];
                var headers = rows[0].split(',');

                for (var i = 1; i < rows.length; i++) {
                    var row = rows[i].split(',');
                    if (row.length === headers.length) {
                        var rowData = {};
                        for (var j = 0; j < headers.length; j++) {
                            rowData[headers[j].trim()] = row[j].trim();
                        }
                        data.push(rowData);
                    }
                }

                $.ajax({
                    url: '/import_csv/',
                    type: 'POST',
                    data: JSON.stringify(data),
                    contentType: 'application/json',
                    success: function (response) {
                        if (response.success) {
                            dt.ajax.reload(); // Reload the DataTable
                            myTable.ajax.reload(null, false);
                        } else {
                            alert('Error importing data.');
                        }
                    },
                    error: function () {
                        alert('Error importing data.');
                    }
                });
            };
            reader.readAsText(file);
        }
    });

    $('#select-all').on('click', function () {
        myTable.rows().select();
    });

    myTable.on('xhr', function (e, settings, json, xhr) {
        console.log('Data received from server:', json);
    });

});
