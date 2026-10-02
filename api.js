/* Same-origin API: run the site through start.sh / start.bat, not file://. */
window.VodaAPI = (() => {
  async function request(path, options = {}) {
    const headers = new Headers(options.headers || {});
    if (options.method && options.method !== 'GET') headers.set('X-Voda-Request', '1');
    if (options.body && !(options.body instanceof FormData)) headers.set('Content-Type', 'application/json');
    const response = await fetch(path, { ...options, headers, credentials: 'same-origin', cache: 'no-store' });
    const data = await response.json().catch(() => null);
    if (!response.ok) {
      const detail = data?.detail;
      const message = typeof detail === 'string' ? detail : response.status === 413 ? '파일이 너무 큽니다.' : `요청에 실패했습니다 (${response.status}).`;
      const error = new Error(message);
      error.status = response.status;
      if (response.status === 401 && !path.endsWith('/login')) window.dispatchEvent(new Event('voda-session-expired'));
      throw error;
    }
    return data;
  }
  return {
    request,
    list: kind => request(`/api/content/${kind}`),
    async save(kind, item, editing) {
      const body = { title: item.title };
      if (kind === 'board') Object.assign(body, {content: item.content, category: item.category, pinned: item.pinned});
      else {
        body.description = item.description;
        body.photos = (item.photos || []).map(photo => ({id: photo.id}));
        if (kind === 'projects') Object.assign(body, {projectCategory: item.projectCategory, link: item.link});
      }
      if (editing) body.updatedAt = item.updatedAt;
      return request(`/api/content/${kind}${editing ? '/' + encodeURIComponent(item.id) : ''}`, {
        method: editing ? 'PUT' : 'POST', body: JSON.stringify(body)
      });
    },
    remove: (kind, item) => request(`/api/content/${kind}/${encodeURIComponent(item.id)}?updatedAt=${item.updatedAt}`, {method: 'DELETE'}),
    async upload(blob) {
      const form = new FormData();
      form.append('file', blob, blob.name || 'photo.png');
      return request('/api/photos', {method: 'POST', body: form});
    }
  };
})();
