type Source = {
  type: string;
  chapter: number;
  verse?: number;
  topic?: string;
};

type Props = {
  sources: Source[];
};

export default function SourceCard({ sources }: Props) {
  if (!sources.length) return null;

  return (
    <div className="mt-5 rounded-2xl border border-orange-200 bg-orange-50 p-4">

      <p className="font-semibold text-orange-600 mb-3">
        📖 Inspired by
      </p>

      <div className="space-y-2">

        {sources.map((source, index) => (

          <div
            key={index}
            className="rounded-xl bg-white px-3 py-2 text-sm shadow-sm"
          >

            {source.type === "verse" ? (
              <>
                Chapter {source.chapter} • Verse {source.verse}
              </>
            ) : (
              <>
                Chapter {source.chapter}
                <br />
                <span className="text-slate-500">
                  {source.topic}
                </span>
              </>
            )}

          </div>

        ))}

      </div>

    </div>
  );
}