import $ from "jquery"
import { groupBy } from "lodash-es"
import people from "./people"
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/js/bootstrap.js'
import 'startbootstrap-sb-admin-2/css/sb-admin-2.css'
import 'startbootstrap-sb-admin-2/js/sb-admin-2.js'
import './style.css'
import './css/all.css'


const managerGroups = groupBy(people, "manager")
const root = document.createElement("div")
root.innerHTML = `<pre>${JSON.stringify(managerGroups, null, 2)}</pre>`


$(document).ready(function () {
    $(".appended").css('color', 'green');
    $('.appended').append(root);
});
