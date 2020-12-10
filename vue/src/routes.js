import Main from "./components/Main";
import Options from "./components/Setup/Options";
import Setup from "./components/Setup/Setup";
import Authenticate from "./components/Setup/Authenticate";
import DataGraph from "./components/Debug/DataGraph";
// import Dashboard from "./components/Dashboard";
import Calendar from "./components/Calendar";
// import MAL from "./components/Settings/MAL";
// import ANIDB from "./components/Settings/ANIDB";
// import Fix_Matching from "./components/Settings/Fix_Matching";
// import Anime from "./components/Settings/Anime";


export default [
  { path: '/main', component: Main,
    children: [
      {path: '/Settings', component: Calendar},
      {path: '/Debug/Graph', component: DataGraph, children: [{path: ':graph_type', component: DataGraph}]}
    ]},
  { path: '/Setup', component: Setup,
    children: [
      {path: '', component: Options},
      {path: 'Options', component: Options},
      {path: 'Authenticate', component: Authenticate,
      children: [
        {path: ':module', component: Authenticate}
      ]}
    ]},
  { path: '*',
    redirect: '/Main' },
  { path: '',
    redirect: '/Main' },
  { path: '/',
    redirect: '/Main' },
];