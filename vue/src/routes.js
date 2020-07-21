import Dashboard from "./components/Dashboard";
import Calendar from "./components/Calendar";
import MAL from "./components/Settings/MAL";
import Shows from "./components/Settings/Shows";

export default [
  { path: '/Dashboard',
    component: Dashboard,},
  { path: '/Calendar',
    component: Calendar,},
  { path: '/Status',
    component: Calendar,},
  { path: '/Settings/Shows',
    component: Shows,},
  { path: '/Settings/MAL',
    component: MAL,},
  { path: '/Settings/MAL/:code',
    component: MAL,},
  { path: '/Settings/Torrent',
    component: Calendar,},
  { path: '/Settings/Plex',
    component: Calendar,},
  { path: '/Settings/MAL',
    redirect: '/Settings/MAL/Watching' },
  { path: '*',
    redirect: '/Dashboard' },
  { path: '',
    redirect: '/Dashboard' },
  { path: '/',
    redirect: '/Dashboard' },
];