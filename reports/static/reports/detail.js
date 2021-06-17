const deleteButton = document.getElementById('delete')
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value
const handleAlerts = (type, msg) => {
    alertBox.innerHTML = `
        <div class="alert alert-${type}" role="alert">
            ${msg}
        </div>
    `
}
deleteButton.addEventListener(onclick(), () => {
    const formData = new FormData()
                    formData.append('csrfmiddlewaretoken', csrf)
                    formData.append('delete', true)
                    $.ajax({
                        type: 'POST',
                        url: 'delete',
                        data: formData,
                        success: function (response) {
                            spinner.classList.add('not-visible')
                            console.log(response)
                            handleAlerts('success', 'Report Generated')
                             window.location.href = "reports";
                        },
                        error: function (error) {
                            console.log(error)
                            handleAlerts('danger', 'Oops... something went wrong')
                        },
                        processData: false,
                        contentType: false,
                    })
})