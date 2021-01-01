import HomePage from '../pages/home.f7.html'
import LoginPage from '../pages/login.f7.html'
import RegisterPage from '../pages/register.f7.html'
import ProfilePage from '../pages/profile.f7.html'
import NewEventPage from '../pages/new-event.f7.html'
import ViewEventPage from '../pages/view-event.f7.html'
import PageNotFound from '../pages/page-not-found.f7.html'
import MyEventsPage from '../pages/my-events.f7.html'
import EditEventPage from '../pages/edit-event.f7.html'
import ApiService from './ApiService'

var routes = [
  {
    path: '/',
    name: 'main',
    component: HomePage,
    keepAlive: true,
    options: {
      reloadCurrent: true
    },
    beforeEnter: function (routeTo, routeFrom, resolve, reject) {
      var router = this
      ApiService.get("current/", function(data) {
        console.log("SUCCESS", data.msg)
        window.sessionStorage.setItem("userId", data.user.id)
        resolve()
      }, function(data) {
        console.log("ERROR", data.msg)
        reject()
        router.navigate('/login')
      })
    }
  },
  {
    path: '/login',
    name: 'login',
    component: LoginPage,
    options: {
      reloadCurrent: true
    }
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterPage,
    options: {
      transition: 'f7-parallax',
      reloadCurrent: true
    }
  },
  {
    path: '/profile',
    name: 'profile',
    popup: { component: ProfilePage }
  },
  {
    path: '/new-event',
    name: 'new-event',
    popup: { component: NewEventPage }
  },
  {
    path: '/view-event/:id',
    popup: { component: ViewEventPage }
  },
  {
    path: '/edit-event/:id',
    name: 'edit-event',
    popup: { component: EditEventPage }
  },
  {
    path: '/my-events',
    name: 'my-events',
    popup: { component: MyEventsPage },
    keepAlive: true,
    options: {
      reloadCurrent: true
    }
  },
  {
    path: '/page-not-found',
    popup: { component: PageNotFound }
  }
]

export default routes
