'use client';

import { useEffect, useMemo, useState } from 'react';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface FilterParameter {
  name: string;
  type: string;
  description: string;
  default?: any;
}

interface FilterDefinition {
  id: string;
  name: string;
  description: string;
  parameters: FilterParameter[];
}

interface ScreenerResult {
  symbol: string;
  company_name: string;
  last_price: number;
  volume: number;
  trade_value: number;
  percent_change: number;
  last_updated: string;
  reason: string;
  score?: number | null;
}

interface SelectedFilter {
  id: string;
  params: Record<string, any>;
}

export default function HomePage() {
  const [filters, setFilters] = useState<FilterDefinition[]>([]);
  const [selected, setSelected] = useState<Record<string, SelectedFilter>>({});
  const [results, setResults] = useState<ScreenerResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetch(`${API_BASE}/api/filters`)
      .then((res) => res.json())
      .then((data: FilterDefinition[]) => {
        setFilters(data);
        const defaults: Record<string, SelectedFilter> = {};
        data.forEach((f) => {
          defaults[f.id] = {
            id: f.id,
            params: f.parameters.reduce<Record<string, any>>((acc, p) => {
              acc[p.name] = p.default ?? '';
              return acc;
            }, {}),
          };
        });
        setSelected(defaults);
      })
      .catch(() => setError('مشکل در دریافت فیلترها'));
  }, []);

  const selectedFilters = useMemo(
    () =>
      Object.values(selected).filter((f) =>
        filters.some((definition) => definition.id === f.id)
      ),
    [selected, filters]
  );

  const handleParamChange = (
    filterId: string,
    paramName: string,
    value: string | number
  ) => {
    setSelected((prev) => ({
      ...prev,
      [filterId]: {
        ...(prev[filterId] || { id: filterId, params: {} }),
        params: { ...(prev[filterId]?.params || {}), [paramName]: value },
      },
    }));
  };

  const toggleFilter = (filterId: string, enabled: boolean) => {
    if (!enabled) {
      const updated = { ...selected };
      delete updated[filterId];
      setSelected(updated);
    } else {
      const definition = filters.find((f) => f.id === filterId);
      setSelected((prev) => ({
        ...prev,
        [filterId]: {
          id: filterId,
          params:
            definition?.parameters.reduce<Record<string, any>>((acc, p) => {
              acc[p.name] = p.default ?? '';
              return acc;
            }, {}) || {},
        },
      }));
    }
  };

  const runScreener = async () => {
    setLoading(true);
    setError('');
    try {
      const payload = {
        filters: selectedFilters,
      };
      const res = await fetch(`${API_BASE}/api/screener/run`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      if (!res.ok) {
        throw new Error('خطا در اجرای فیلتر');
      }
      const data: ScreenerResult[] = await res.json();
      setResults(data);
    } catch (e) {
      setError('اجرای فیلتر با مشکل مواجه شد');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="space-y-6">
      <header className="bg-white shadow rounded-xl p-6">
        <h1 className="text-2xl font-bold mb-2">bestamoozscreener</h1>
        <p className="text-sm text-slate-600">
          فیلترنویسی سریع برای نمادهای بورس ایران - نسخه MVP
        </p>
      </header>

      <section className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="lg:col-span-1 space-y-4">
          <div className="bg-white rounded-xl shadow p-4">
            <h2 className="font-semibold mb-3">فیلترهای آماده</h2>
            <div className="space-y-3">
              {filters.map((filter) => {
                const enabled = Boolean(selected[filter.id]);
                return (
                  <div
                    key={filter.id}
                    className="border rounded-lg p-3 hover:border-indigo-300"
                  >
                    <div className="flex items-start justify-between gap-2">
                      <div>
                        <p className="font-semibold">{filter.name}</p>
                        <p className="text-xs text-slate-600">
                          {filter.description}
                        </p>
                      </div>
                      <input
                        type="checkbox"
                        checked={enabled}
                        onChange={(e) => toggleFilter(filter.id, e.target.checked)}
                        className="h-4 w-4 mt-1"
                      />
                    </div>

                    {enabled && filter.parameters.length > 0 && (
                      <div className="grid grid-cols-2 gap-2 mt-3">
                        {filter.parameters.map((param) => (
                          <label
                            key={param.name}
                            className="flex flex-col text-xs gap-1"
                          >
                            <span className="text-slate-600">{param.description}</span>
                            <input
                              type="number"
                              defaultValue={param.default as any}
                              onChange={(e) =>
                                handleParamChange(
                                  filter.id,
                                  param.name,
                                  param.type === 'int'
                                    ? parseInt(e.target.value, 10)
                                    : parseFloat(e.target.value)
                                )
                              }
                              className="border rounded px-2 py-1 text-sm"
                            />
                          </label>
                        ))}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>

          <button
            onClick={runScreener}
            disabled={loading || selectedFilters.length === 0}
            className="w-full bg-indigo-600 text-white rounded-lg py-2 font-semibold hover:bg-indigo-700 disabled:bg-slate-400"
          >
            {loading ? 'در حال پردازش...' : 'اعمال فیلتر'}
          </button>
          {error && <p className="text-red-600 text-sm">{error}</p>}
        </div>

        <div className="lg:col-span-2">
          <div className="bg-white rounded-xl shadow p-4">
            <div className="flex items-center justify-between mb-3">
              <h2 className="font-semibold">نتایج</h2>
              <p className="text-xs text-slate-500">
                {results.length > 0
                  ? `${results.length} نماد مطابق`
                  : 'هنوز فیلتری اجرا نشده است'}
              </p>
            </div>
            <div className="overflow-auto">
              <table className="min-w-full text-sm">
                <thead className="bg-slate-100 text-slate-700">
                  <tr>
                    <th className="px-3 py-2 text-left">نماد</th>
                    <th className="px-3 py-2 text-left">نام شرکت</th>
                    <th className="px-3 py-2 text-left">آخرین قیمت</th>
                    <th className="px-3 py-2 text-left">حجم</th>
                    <th className="px-3 py-2 text-left">ارزش معاملات</th>
                    <th className="px-3 py-2 text-left">درصد تغییر</th>
                    <th className="px-3 py-2 text-left">آخرین بروزرسانی</th>
                    <th className="px-3 py-2 text-left">علت تطابق</th>
                  </tr>
                </thead>
                <tbody>
                  {results.map((row) => (
                    <tr key={row.symbol} className="border-b hover:bg-slate-50">
                      <td className="px-3 py-2 font-semibold">{row.symbol}</td>
                      <td className="px-3 py-2">{row.company_name}</td>
                      <td className="px-3 py-2">{row.last_price.toLocaleString()}</td>
                      <td className="px-3 py-2">{row.volume.toLocaleString()}</td>
                      <td className="px-3 py-2">{row.trade_value.toLocaleString()}</td>
                      <td className="px-3 py-2">{row.percent_change}%</td>
                      <td className="px-3 py-2">
                        {new Date(row.last_updated).toLocaleString('fa-IR')}
                      </td>
                      <td className="px-3 py-2 text-indigo-700">{row.reason}</td>
                    </tr>
                  ))}
                  {results.length === 0 && (
                    <tr>
                      <td className="px-3 py-6 text-center text-slate-500" colSpan={8}>
                        نتیجه‌ای برای نمایش وجود ندارد.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}
