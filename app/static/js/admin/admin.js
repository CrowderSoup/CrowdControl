define(function (require) {
    var path = location.pathname.replace('/admin', '').replace(/\d+/g, '').replace(/\/$/, '');

    var vm = null;
    switch (path) {
        case "/pages":
            vm = require('pages/index');
            break;
        case "/pages/page":
            vm = require('pages/edit_page');
            break;
        case "/pages/new":
            vm = require('pages/add_page');
            break;
        case "/blog/posts":
            vm = require('posts/index');
            break;
        case "/blog/posts/post":
            vm = require('posts/edit_post');
            break;
        case "/blog/posts/new":
            vm = require('posts/add_post');
            break;
        case "/blog/categories/category":
            vm = require('posts/add_edit_category');
            break;
        case "/blog/categories/new":
            vm = require('posts/add_edit_category');
            break;
        case "/menus":
            vm = require('menus/menus');
            break;
        case "/menus/menu":
            vm = require('menus/menu');
            break;
        case "/menus/menu/new":
            vm = require('menus/new');
            break;
        case "/menus/menu/menu-item":
            vm = require('menus/menu-item/menu-item');
            break;
        case "/menus/menu/menu-item/new":
            vm = require('menus/menu-item/new');
            break;
        default:
            vm = require('pages/index');
            break;
    }

    if (_.isFunction(vm)) {
        vm = new vm();
    } else {
        toastr.error("Unable to load page. Please refresh and try again.");
    }

    if (vm !== null && vm.canActivate()) {
        vm.activate();
    }

    ko.applyBindings(vm);

});
