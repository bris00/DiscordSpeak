from lib.discordspeak import Module

q, w, e, r, t, y, u, i, o, p, a, s, d, f, g, h, j, k, l, z, x, c, v, b, n, m = 'qwertyuiopasdfghjklzxcvbnm'

keyboard_near = dict(
    q=[w, s, a],
    w=[q, a, s, e],
    e=[w, d, r],
    r=[e, d, f, t],
    t=[r, f, g, y],
    y=[t, g, h, u],
    u=[y, h, j, i],
    i=[u, j, k, o],
    o=[i, k, l, p],
    p=[o, l],
    a=[q, w, s, z],
    s=[w, a, x, d, e],
    d=[e, s, x, c, f],
    f=[r, d, c, v, g, t],
    g=[t, f, v, b, h, y],
    h=[y, g, b, n, j, u],
    j=[u, h, n, m, k, i],
    k=[i, j, m, l, o],
    l=[o, k],
    z=[a, s, x],
    x=[z, s, d, c],
    c=[x, d, f, v],
    v=[c, f, g, b],
    b=[v, g, h, n],
    n=[b, h, j, m],
    m=[n, j, k],
)

class SpellingMistakes(Module):
    def on_key(self, key):
        if helpers.chance(1/100):
            if key.name not in keyboard_near or helpers.chance(1/2):
                return []
            else:
                return [random.choice(keyboard_near[key.name])]