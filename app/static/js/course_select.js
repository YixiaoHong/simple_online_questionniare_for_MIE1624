var display_all_courses;
var display_all_selected_courses;
var add_selected_courses;
var delete_selected_courses;
var categories;
var all_courses;
var search_bar;
var error_msg;
var selected_courses_ctr;
var selected_courses_limit = 10;
var selected_courses_ctr_counter = 0;
var selected_categories = [];
var selected_course_color = 'white';

function prevent_add_too_many_courses(add_course_list) {
    console.log("INT: " + selected_courses_ctr.getAttribute("value"));
    var selected_courses_ctr_counter_curr = parseInt(selected_courses_ctr.getAttribute("value")) + selected_courses_ctr_counter;
    console.log(add_course_list.length + parseInt(selected_courses_ctr_counter_curr));
    console.log(parseInt(selected_courses_limit));
    if (add_course_list.length + parseInt(selected_courses_ctr_counter_curr) > parseInt(selected_courses_limit)) {
        return false;
    } else {
        return true;
    }
}

function count_selected_courses() {
    selected_courses_ctr_counter = 0;
    for (var i = 0; i < all_courses.length; i++) {
        let curr_course = all_courses[i];
        if (curr_course.parentNode.parentNode.parentNode.getAttribute("id") === "display_all_selected_courses") {
            selected_courses_ctr_counter++;
        }
    }
    return selected_courses_ctr_counter;

}

function add_selected() {
    var selected_courses = display_all_courses.querySelectorAll('.all_courses:checked');
    console.log("CTR: " + selected_courses.length);
    var is_valid = prevent_add_too_many_courses(selected_courses);
    if (is_valid) {
        var orig_ctr = count_selected_courses();
        selected_courses.forEach(function (course) {
            course.checked = false;
            display_all_selected_courses.insertAdjacentElement("beforeend", course.parentNode.parentNode)
        });
        var after_ctr = count_selected_courses();
        clean_all_courses_color();
        selected_courses_ctr.innerHTML = parseInt(selected_courses_ctr.innerHTML) + (after_ctr - orig_ctr);
    } else {
        error_msg.innerHTML = "Too many courses: exceed the max course load";
    }

}

function delete_selected() {
    var selected_courses = display_all_selected_courses.querySelectorAll('.all_courses:checked');
    var orig_ctr = count_selected_courses();
    selected_courses.forEach(function (course) {
        course.checked = false;
        display_all_courses.insertAdjacentElement("beforeend", course.parentNode.parentNode);
    });
    var after_ctr = count_selected_courses();
    clean_all_courses_color();
    selected_courses_ctr.innerHTML = parseInt(selected_courses_ctr.innerHTML) + (after_ctr - orig_ctr);
}

function update_courses_list_by_category() {
    for (let j = 0; j < all_courses.length; j++) {
        let par = all_courses[j].parentNode.parentNode;
        if (par.parentNode.getAttribute("id") === display_all_courses.getAttribute("id")) {
            par.style.display = "none";
        }
    }
    for (let i = 0; i < selected_categories.length; i++) {
        for (let j = 0; j < all_courses.length; j++) {
            let curr_categories = all_courses[j].getAttribute("class");
            if (curr_categories.includes(selected_categories[i])) {
                let par = all_courses[j].parentNode.parentNode;
                if (par.parentNode.getAttribute("id") === display_all_courses.getAttribute("id")) {
                    par.style.display = "block";
                }
            }
        }
    }
}

function update_table() {
    let keyword = search_bar.value;
    if (keyword.length === 0) {
        for (let j = 0; j < all_courses.length; j++) {
            let par = all_courses[j].parentNode.parentNode;
            if (par.parentNode.getAttribute("id") === display_all_courses.getAttribute("id")) {
                par.style.display = "block";
            }
        }
    } else {
        update_courses_list_by_typing(keyword);
    }
}

function update_courses_list_by_typing(keyword) {
    for (let j = 0; j < all_courses.length; j++) {
        let par = all_courses[j].parentNode.parentNode;
        if (par.parentNode.getAttribute("id") === display_all_courses.getAttribute("id")) {
            par.style.display = "none";
        }
    }
    for (let j = 0; j < all_courses.length; j++) {
        let curr_name = all_courses[j].parentNode.textContent;
        if (curr_name.toLowerCase().includes(keyword.toLowerCase())) {
            let par = all_courses[j].parentNode.parentNode;
            if (par.parentNode.getAttribute("id") === display_all_courses.getAttribute("id")) {
                par.style.display = "block";
            }
        }
    }
}

function init() {
    display_all_courses = document.getElementById("display_all_courses");
    display_all_selected_courses = document.getElementById("display_all_selected_courses");
    add_selected_courses = document.getElementById("add_selected_courses");
    categories = document.getElementsByClassName("categories");
    delete_selected_courses = document.getElementById("delete_selected_courses");
    all_courses = document.getElementsByClassName("all_courses");
    search_bar = document.getElementById("search_bar");
    selected_courses_ctr = document.getElementById("selected_courses_ctr");
    error_msg = document.getElementById("error_msg");



    add_selected_courses.addEventListener("click", add_selected, false);
    delete_selected_courses.addEventListener("click", delete_selected, false);
    search_bar.addEventListener("input", update_table, false);
    for (let i = 0; i < categories.length; i++) {
        let category = categories[i];
        category.checked = true;
        selected_categories.push(category.value);
        category.addEventListener("change", function () {
            search_bar.value = "";
            if (this.checked) {
                selected_categories.push(this.value)
            } else {
                var index = selected_categories.indexOf(this.value);
                if (index > -1) {
                    selected_categories.splice(index, 1);
                }
            }
            update_courses_list_by_category()
        }, false)
    }
    for (let i = 0; i < all_courses.length; i++) {
        let curr_course = all_courses[i];
        curr_course.addEventListener("change", function () {
            if (this.checked) {
                this.parentNode.parentNode.style.background = selected_course_color;
            } else {
                this.parentNode.parentNode.style.background = 'transparent';
            }
        }, false);
    }
}

function submit_() {
    $('#regForm').css('display', 'none');
    $("#loading").css('display', 'inline-block');
    $("#loading").position({
       my: "center",
       at: "center",
       of: window
    });
    $('#display_all_courses').remove();
    $("#regForm").submit();
}

function clean_all_courses_color() {
    for (let i = 0; i < all_courses.length; i++) {
        let curr_course = all_courses[i];
        curr_course.parentNode.parentNode.style.background = 'transparent';

    }
}

window.addEventListener("load", init, false);