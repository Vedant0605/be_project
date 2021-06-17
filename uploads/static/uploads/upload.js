const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value
const alertBox = document.getElementById('alert-box')
const loadingSpinner = document.getElementById('spinner')

const handleAlerts = (type, msg) => {
    alertBox.innerHTML = `
        <div class="alert alert-${type}" role="alert">
            ${msg}
        </div>
    `
}

Dropzone.autoDiscover = false
const myDropzone = new Dropzone('#my-dropozne', {
    url: 'generate',
    init: function () {
        this.on('sending', function (file, xhr, formData) {
            console.log('sending')
            formData.append('csrfmiddlewaretoken', csrf)
        })
        this.on('success', function (file, response) {
            console.log(response)
            spinner.classList.toggle('not-visible')
            if (response.ex) {
                handleAlerts('danger', 'File already exists')
                if (response.already) {

                } else {
                    const formData = new FormData()
                    formData.append('csrfmiddlewaretoken', csrf)
                    formData.append('file_name', response.file_name)
                    formData.append('changed_file_name', response.changed_file_name)
                    formData.append('upload_id', response.upload_id)
                    $.ajax({
                        type: 'POST',
                        url: 'report',
                        data: formData,
                        success: function (response) {
                            spinner.classList.add('not-visible')
                            console.log(response)
                            handleAlerts('success', 'Report Generated')
                            reportForm.reset()
                        },
                        error: function (error) {
                            spinner.classList.add('not-visible')
                            console.log(error)
                            handleAlerts('danger', 'Oops... something went wrong')
                        },
                        processData: false,
                        contentType: false,
                    })
                }
            } else {
                handleAlerts('success', 'Your file has been uploaded')
                const formData = new FormData()
                formData.append('csrfmiddlewaretoken', csrf)
                formData.append('file_name', response.file_name)
                formData.append('changed_file_name', response.changed_file_name)
                formData.append('upload_id', response.upload_id)
                $.ajax({
                    type: 'POST',
                    url: 'report',
                    data: formData,
                    success: function (response) {
                        spinner.classList.add('not-visible')
                        console.log(response)
                        handleAlerts('success', 'Report Generated')
                        reportForm.reset()
                    },
                    error: function (error) {
                        spinner.classList.add('not-visible')
                        console.log(error)
                        handleAlerts('danger', 'Oops... something went wrong')
                    },
                    processData: false,
                    contentType: false,
                })
            }
        })
    },
    maxFiles: 1,
    maxFilesize: 3000,
    acceptedFiles: '.mp4'
})

