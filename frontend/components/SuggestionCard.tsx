type Props = {
  text: string;
  onClick: () => void;
};

export default function SuggestionCard({ text, onClick }: Props) {
  return (
    <button
      onClick={onClick}
      className="rounded-2xl border border-slate-200 bg-white p-5 text-left shadow-sm hover:shadow-md hover:-translate-y-1 transition w-full"
    >
      {text}
    </button>
  );
}