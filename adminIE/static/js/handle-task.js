
function handleTask(task_id) {
    var timer = setTimeout(function f(task_id) {
        // alert(task_id)   
        // 传递的task_id
        // console.log(task_id)
        $.getJSON(`/octopus/get_task/?task_id=${task_id}`,
            function (res) {
                console.log(res)
                if (res.success) {
                    $("#result").append(
                        `<code>${res.id}</code><code>${res.status}</code>
                        <code>任务结果${res.result}</code>`
                    );
                    clearTimeout(timer);
                } else {
                    $("#result").append(
                        `<code>${res.id}</code><code>${res.status}</code><code>任务结果${res.result.success}</code>`
                    );
                };
            }
        ), timer = setTimeout(f, 2000, task_id);
    }, 2000, task_id)

}
