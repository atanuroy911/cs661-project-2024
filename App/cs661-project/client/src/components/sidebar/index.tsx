"use client";
import {
  LucideIcon,
  LayoutDashboard,
  AudioWaveform,
  ScatterChart,
  GitGraph,
  BadgePercent,
  PieChart
} from "lucide-react";
import SidebarItem from "./item";

interface ISidebarItem {
  name: string;
  path: string;
  icon: LucideIcon;
  items?: ISubItem[];
}

interface ISubItem {
  name: string;
  path: string;
}

const items: ISidebarItem[] = [
  {
    name: "WordCloud",
    path: "/",
    icon: LayoutDashboard,
  },
  {
    name: "Song Similarity",
    path: "/similarity",
    icon: BadgePercent,
  },
  {
    name: "Topic modelling",
    path: "/topicmodelling",
    icon: GitGraph,
    items: [
          {
            name: "General",
            path: "/topicmodelling",
          },
          {
            name: "All Topics",
            path: "/topicmodelling/all",
          },
        ],
  },
  {
    name: "Rhyme Analysis",
    path: "/rhyme",
    icon: AudioWaveform,
  },
  {
    name: "Lyricist Similarity",
    path: "/lyricistsimilarity",
    icon: ScatterChart,
  },
  {
    name: "POS Analysis",
    path: "/posanalysis",
    icon: PieChart,
  },
  // {
  //   name: "Settings",
  //   path: "/settings",
  //   icon: Settings,
  //   items: [
  //     {
  //       name: "General",
  //       path: "/settings",
  //     },
  //     {
  //       name: "Security",
  //       path: "/settings/security",
  //     },
  //     {
  //       name: "Notifications",
  //       path: "/settings/notifications",
  //     },
  //   ],
  // },
];

const Sidebar = () => {
  return (
    <div className="fixed top-0 left-0 h-screen w-64 bg-white shadow-lg z-10 p-4">
      <div className="flex flex-col space-y-10 w-full">
        <img className="h-10 w-fit" src="/logo.png" alt="Logo" />
        <div className="flex flex-col space-y-2">
          {items.map((item, index) => (
            <SidebarItem key={index} item={item} />
          ))}
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
