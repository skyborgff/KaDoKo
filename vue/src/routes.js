import Main from "./components/Main";
import Options from "./components/Setup/Options";
import Setup from "./components/Setup/Setup";
import Authenticate from "./components/Setup/Authenticate";
import DataGraph3D from "./components/Debug/DataGraph3D";
import Settings from "./components/Settings/Settings"
import Providers from "./components/Settings/Providers/Providers"
import AnimeSettings from "./components/Settings/Anime/AnimeSettings"


export default [
  { path: '/main', component: Main,
    children: [
      { path: '/Settings', component: Settings, children:
          [{ path: 'providers', component: Providers}, { path: 'anime', component: AnimeSettings}]},
      { path: '/Debug/Graph', component: DataGraph3D, children: [{path: ':graph_type', component: DataGraph3D}]}
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