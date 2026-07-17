type Props = {
  onNewChat: () => void;
};

export default function Navbar({ onNewChat }: Props) {
  return (
    <nav className="w-full flex items-center justify-between py-6">

      <h1 className="text-2xl font-bold text-slate-800">
        🪷 KrishnaGPT
      </h1>

      <button
        onClick={onNewChat}
        className="rounded-full border px-4 py-2 text-sm hover:bg-orange-50 transition"
      >
        New Conversation
      </button>

    </nav>
  );
}