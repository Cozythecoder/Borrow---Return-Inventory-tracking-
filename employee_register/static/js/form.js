$(document).ready(function () {
    $('#datatable_employee').DataTable({
      paging: false,
      info: false,
      order: [[0, 'desc']],
      "dom": '<"myTable"t>',
      // Add any configuration options here
      ajax: {
        url: '/ajax_list/',
        dataSrc: function (json) {
          // Slice the last 15 records from the data
          return json.slice(-15);
        },
        error: function (jqXHR, textStatus, errorThrown) {
          console.error('Error loading data: ', textStatus, errorThrown);
        }
      },

      columns: [
        { data: 'id', className: 'text-center' },
        {
          data: "emp_id", // Use emp_id to reference the employee
          title: "Fullname",
          render: function (empId, type, row, meta) {
            const fullname = row.fullname; // Get fullname directly from the row data
            const paddedEmpId = empId ? empId.toString().padStart(6, '0') : '';

            return fullname ? `<div class="svg-text-container"> 
            <svg class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 24 24">
                <path fill-rule="evenodd" d="M12 4a4 4 0 1 0 0 8 4 4 0 0 0 0-8Zm-2 9a4 4 0 0 0-4 4v1a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2v-1a4 4 0 0 0-4-4h-4Z" clip-rule="evenodd"/>
            </svg>
            <span>${fullname} (ID: ${paddedEmpId})</span>
        </div>` : '';
          }
        },
        { data: 'model', className: 'text-center' },
        { data: 'asset_tag', className: 'text-center' },
        { data: 'duration', className: 'text-center' },
        { data: 'status', className: 'text-center' },
        { data: 'return_by', className: 'text-center' },
        {
          data: "created_at",
          title: "Created at",
          render: function (data, type, row, meta) {
            return data ? `
            <div style="text-align: center;">
                <div class="svg-text-container">
                    <svg class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
                        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"/>
                    </svg>
                    <span>${data}</span>
                </div>
            </div>
          ` : '';
          },
          className: 'text-center',
          datetimepicker: { format: "Y-m-d H:i:00" }
        }
      ],
      exportOptions: {
        modifer: {
          page: '10',
          search: 'none'
        }
      },
      createdRow: function (row, data, dataIndex) {
        $(row).addClass('tbody-color table-striped');
        // Change background color of the 'status' column based on the status value
        if (data.status === 'Pending') {
          $('td:eq(5)', row).css('background-color', 'rgba(255, 0, 0, 0.5)');  // Red with 50% opacity
        } else {
          $('td:eq(5)', row).css('background-color', 'rgba(0, 128, 0, 0.5)'); // Green with 50% opacity
        }
      }
    });

    $('#borrow_fullname').select2({
      ajax: {
        url: '/staff_list_search/',
        dataType: 'json',
        delay: 250,
        processResults: function (data) {
          return {
            results: $.map(data, function (item) {
              return {
                id: item.fullname,
                text: item.fullname + ' (ID: ' + item.emp_id.toString().padStart(6, '0') + ')',
                model: item.model,
              };
            })
          };
        },
        cache: true,
      },
      placeholder: 'Select Your Name',
      allowClear: true,
      searchInputPlaceholder: 'Type to search...'
    });


    $('#borrow_fullname').on('select2:open', function () {
      var searchField = $('.select2-search__field');
      if (searchField.length) {
        searchField[0].focus();
      }
    });

    $('#borrow_fullname').on('select2:select', function (e) {
      var selectedData = e.params.data; // Get selected data
      var empId = selectedData.text.match(/\(ID: (\d{6})\)/); // Extract emp_id using regex

      if (empId) {
        $('#borrow_emp_id').val(empId[1]); // Set the emp_id in the hidden field
      }
    });

    $('#borrow_asset_tag').select2({
      ajax: {
        url: '/equipment_list_search/',
        dataType: 'json',
        delay: 250,
        processResults: function (data) {
          return {
            results: $.map(data, function (item) {
              return {
                id: item.asset_tag,
                text: item.asset_tag + ' ( ' + item.display_name + ' )'
              };
            })
          };
        },
        cache: true
      },
      placeholder: 'Select an Asset Tag',
      allowClear: true,
      searchInputPlaceholder: 'Type to search...',
      minimumInputLength: 1
    });

    $('#borrow_asset_tag').on('select2:open', function () {
      var searchField = $('.select2-search__field');
      if (searchField.length) {
        searchField[0].focus();
      }
    });


    $('#return_fullname').select2({
      ajax: {
        url: '/staff_list_search/',
        dataType: 'json',
        delay: 250,
        processResults: function (data) {
          return {
            results: $.map(data, function (item) {
              return {
                id: item.fullname,
                text: item.fullname + ' (ID: ' + item.emp_id.toString().padStart(6, '0') + ')'
              };
            })
          };
        },
        cache: true
      },
      placeholder: 'Select Your Name',
      searchInputPlaceholder: 'Type to search...',
      allowClear: true,
    });

    $('#return_fullname').on('select2:open', function () {
      var searchField = $('.select2-search__field');
      if (searchField.length) {
        searchField[0].focus();
      }
    });

    $('#return_fullname').on('select2:select', function (e) {
      var selectedData = e.params.data; // Get selected data
      var empId = selectedData.text.match(/\(ID: (\d{6})\)/); // Extract emp_id using regex

      if (empId) {
        $('#return_emp_id').val(empId[1]); // Set the emp_id in the hidden field
      }
    });

    $('#return_asset_tag').select2({
      ajax: {
        url: '/equipment_list_search/',
        dataType: 'json',
        delay: 250,
        processResults: function (data) {
          return {
            results: $.map(data, function (item) {
              return {
                id: item.asset_tag,
                text: item.asset_tag + ' ( ' + item.display_name + ' )',
                model: item.model,
              };
            })
          };
        },
        cache: true
      },
      placeholder: 'Select an Asset Tag',
      allowClear: true,
      searchInputPlaceholder: 'Type to search...',
      minimumInputLength: 1
    });

    $('#return_asset_tag').on('select2:open', function () {
      var searchField = $('.select2-search__field');
      if (searchField.length) {
        searchField[0].focus();
      }
    });
  });