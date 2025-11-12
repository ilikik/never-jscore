import never_jscore

ctx = never_jscore.Context(enable_extensions=True)

# 示例1: Hook XMLHttpRequest.send 拦截加密数据
# result = ctx.evaluate(js)
result = ctx.evaluate('''
     var kN = "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";
    var D0 = kN;
    var rP = window.atob(D0);
    var RQ = 0;
    var lx = rP.length;
    var Cx = [];
    while (RQ < lx) {
        var AY = rP.charCodeAt(RQ);
        Cx.push(AY);
        RQ += 1
    }
    var M1 = [];
    var oo = 0;
    var la = "0xUSUFPUWZxamVhZHthZWRlZGZxYm9lZU1gem9sIUZyc25yL3B1Y2NrZWR0UWJxYW1kdWZzYnFlYHVmQXZmZWZyf2VkdFVpbWduYmlnYHRxd3BrWF10ZDgwMSxddGZiZmVcJWhlZmx1amVpZnNlZHdPdmxSc2xxZnB1eEVnc2JxaHB3bnNjbmx1YWptZnBWUUlCT0RNR19QVlFIUU1ERUlVT15ET01AVUJST0xSU05jbGV5YGxvX1xyc2x3b19ebWFtZGVIdWVtam5tZnBJZWtkaHZxZmxlZnFkZkF2ZmVmcU9ub2x1eHFnQ25zcWp1Y2VkdWJ1YWhsSWVrZGh2T2wjVUNRT25sd213YGtwdWJwd2ptZWVNQFteRlFDRU1GTFddVk1KR05RT15VR0BXTlNQPWpmcWFtZCNyc2Bnb2E9Mjw/LWpmcWFtZj9XbnNpZnFgcHFmbGdAaWhsZGVmZWptZFJzbHFmcHV4ZWdzYnFocHVrbm5zZmAqMTU0LjE1NCwxK1BJQEVKT0dcTUJPRVVDRUdeVUZTUUtOTWpvcHVibHVpYHVlamxtam1kZWB1YW9ub29wcWNhZ2NubHVmbHRHb2F1bWZsdHZxdm9jZWR2QWB0dWZxenFgdWttbWpvU1dAdG4vU1dAdG9YZWRwdGggbWltaHVea21qb1VMUG1heWZyL09AW3FrYmFjcWZRZW9udWdAaWhsZ11kNjEyYmIxOTEwcHQhQnFpYG5RRkxFRlFGUmVobG5RZ2B3cXZhYnJxYXtpZXtwcG13ZWpvcEVEUFRLXkFIV1NzYnFlZmxZd3FmcUNlZmx0VEdDQHRuLFRHQ0B0b2Vkd0NubHVkeHVAdHZxamF0dWdzX191ZmBmcWp1ZnNfc2JxaHB3XmV2b2B1a25vZWR3QGlibm1kbEVgdWBxYnNxZUpsdEdvYXVtZmx0VWltZG1qbWdjbm5tZ2B1a25tTUBbX0NNTkFKTURHXFVEWFVWUUddSU1DRUddVk1IV1AvcHZxam9kI2FjcHQiZWFobWRkc290dWdwdWR4dWZybWBscWh5ZGxFZHB0aWJ1YWhsTWZkdWh1ZnFgdWtub3NecWJucWBlaXdxWkV2b2B1a25scWJzcWYwZ2RvbmFgb0NtbHNvcWh1Z0xxZnFgdWtubWNgdXVgbkNtdmxlam9mQ2x6UWtkaHVhdGVrbVwrWl1tZWNxdnFkVWR4dHFmcW1rc3Frbm9zdWZjZG4xd3FkUnNvZnFhblNGQUB3bXdgaWZsZ2VkdUB0dnFqYXR1ZElhZHR1Zm9zYGt1ZWhtZnFWTU1DU0lER15RRkxFRlFGU19VRkNET2djcWJjcUJ1Ymx3RWJwZWZDakBWdWhlZ28vb2dnOCNjbGVnY3E+IHRpZ25xYiNicUBnbGZiL1B2cWVhbmZxZXF1Zm9heElLREtdSkxWcHR2Z25xRWNga3F5bmNsbW9td3FldHFPU010dG9vb2htYm9ldWNlZnVoZWdvLWxwNzgjY2xlZ2NxPiFid2EyLDYxRDExRiFDYnNsUEZGLFBGRHdtd2BrYWJvYWRvcXZjcHZxam9kSUROVW1pbWRVeHFncWltY2VnL3VmYHF2b2pvb3ZvUGlkbG4tVUhJZGxxZnFNY2JzbW1kZWliRG1jcGhRYHFmci1NY2JzbW1kZWliRG1jcGhRYHFmcHJxZ2FrcWtubCFtZGVpdWxwImRvbWB3OnVicXlqb2QidWdiMCJ1YnF5amxVZHtDb25wZWptYHVnOndtaGQhbWFqbCkoI3tkb15GcWNnQ2xvbnE+dWdgNCp1YnF5amxVZHtDb25wZWptYHVkLDAtMSs5fmVobGxVZHh3ZWR0VWltZntubWdOZmdxZHdlZHdQaWBlZnBScWdha3Frbm5HbnFtYHdxZG1mbWl1bDJxZW9udWdAaWhsZWh1ZW9RanlmRlFDRU1GTFdfUElARUZTd3BQRkYsUGZnQHZwbHJzbHdsdXhxZ3NicWVmbVlMVUR4dnFgcWJxZmx1RG1lbWZsdGVqdWZtYmBtZGRQbXdlam5zbHVgdWtubUJvZG1nYWFoa3NpaHBxZGVEWFdcdWR4dXZxZ15laGx1ZnNdYm1rc2x2c2xxa2NganNtbWd1ZmBmcWp1ZnEtZnVgbXVgdWVdK1ticWVgdWVEbWVtZmx3cWVic2BrUFVAVUtDXEZRQ1ZFdHV2cWFMZkBXcHZxam9kI2FjcHY4I0Q==";
    var HN = la;
    var cy = window.atob(HN);
    var sB = [];
    var xH = 0;
    var kD = cy.length;
    while (xH < kD) {
        var CI = cy.charCodeAt(xH);
        sB.push(CI);
        xH += 1
    }
    var JJ = sB;

    function Es(U8, Ay) {
        var wo = U8.length;
        var sV = Ay % wo;
        var gM = [];
        var LV = 0;
        while (LV < wo) {
            gM.push(U8[(LV + wo - sV) % wo]);
            LV += 1
        }
        return gM
    }

    function eH(R6, pI) {
        var Vy = pI % 7 + 1;
        var au = [];
        var mu = R6.length;
        var Hw = 0;
        while (Hw < mu) {
            au.push((R6[Hw] >> Vy | R6[Hw] << 8 - Vy) & 255);
            Hw += 1
        }
        return au
    }

    var lz = Es(eH(eH(JJ, 20), 139), 178);
    var XQ = lz;
    var Qq = 0;
    var dB = XQ.length;
    var kS = [];
    while (Qq < dB) {
        var lS = XQ[Qq];
        var Om = window.String.fromCharCode(lS);
        kS.push(Om);
        Qq += 1
    }
    var ml = kS.join("");
    var r2 = "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";
    var N1 = r2;
    var o9 = window.atob(N1);
    var Pk = o9.length;
    var zi = 0;
    while (zi < Pk) {
        var Z5 = o9.charCodeAt(zi);
        M1.push(Z5);
        zi += 1
    }
    var gq = M1;

    function BJ(bE, Xi) {
        var zP = [];
        var DP = 113;
        var g7 = Xi.length;
        var xP = bE.length;
        var gQ = 0;
        while (gQ < xP) {
            var Tv = DP;
            var uW = bE[gQ];
            var uQ = Xi[gQ % g7];
            DP = uW;
            zP.push(uW ^ uQ ^ Tv);
            gQ += 1
        }
        return zP
    }

    var h1 = ml;

    function RV(QJ, m9) {
        var Ju = [];
        var Th = QJ.length;
        var rJ = m9.length;
        var vh = 0;
        while (vh < Th) {
            var QY = QJ[vh];
            var WZ = m9[vh % rJ] & 127;
            Ju.push((QY + 256 - WZ) % 256 ^ 128);
            vh += 1
        }
        return Ju
    }

    var ai = eH(BJ(RV(RV(gq, [117, 221, 76, 164, 137, 98, 223, 186, 213, 156, 9, 18, 18, 48, 2, 91, 133, 68, 149, 183, 68, 158, 100, 153, 26, 107, 13, 247, 61]), [104, 240, 114, 157, 100, 193, 203, 232, 52, 116, 205, 34, 213, 58, 72, 5, 232, 6, 173, 144, 37, 20, 249]), [139, 20, 16, 30, 120, 128, 204, 98, 188, 176, 25, 237, 232, 90, 88, 210, 208, 34, 57]), 178);
    var CQ = ai;
    var pW = [];
    var BZ = CQ.length;
    while (oo < BZ) {
        var Wb = CQ[oo];
        var ln = window.String.fromCharCode(Wb);
        pW.push(ln);
        oo += 1
    }
    var iB = pW.join("");
    var Qx = iB;
    var l8 = Cx;
    var l4 = BJ(BJ(Es(l8, 48), [203, 232, 52, 116, 205, 34, 213, 58, 72, 5, 232, 6, 173, 144, 37, 20, 249, 117, 221, 76, 164, 137, 98, 223, 186, 213, 156, 9, 18, 18]), [178, 139, 20, 16, 30, 120, 128, 204, 98, 188, 176, 25, 237, 232, 90, 88, 210, 208, 34, 57, 104, 240, 114, 157, 100, 193]);
    var mj = [];
    var Lx = l4;
    var Fx = Lx.length;
    var nf = 0;
    while (nf < Fx) {
        var ar = Lx[nf];
        var cz = window.String.fromCharCode(ar);
        mj.push(cz);
        nf += 1
    }
    var uf = "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";
    var dP = uf;
    var Gb = window.atob(dP);
    var vr = Gb.length;
    var S3 = [];
    var Vz = 0;
    while (Vz < vr) {
        var XZ = Gb.charCodeAt(Vz);
        S3.push(XZ);
        Vz += 1
    }
    var kg = S3;
    var Xv = mj.join("");
    var uq = Xv;
    var Ip = RV(BJ(Es(kg, 18), [193, 203, 232, 52, 116, 205, 34, 213, 58, 72, 5, 232, 6, 173, 144, 37, 20, 249, 117, 221, 76, 164, 137, 98, 223, 186, 213, 156, 9, 18]), [178, 139, 20, 16, 30, 120, 128, 204, 98, 188, 176, 25, 237, 232, 90, 88, 210, 208, 34, 57, 104, 240, 114, 157, 100]);
    var Hn = Ip;
    var Je = [];
    var Z3 = 0;
    var QK = Hn.length;
    while (Z3 < QK) {
        var db = Hn[Z3];
        var HV = window.String.fromCharCode(db);
        Je.push(HV);
        Z3 += 1
    }
    var hM = Je.join("");
    var oF = hM;
    var gW = window[Qx.substr(634, 8)];

    function qm(jg, D_) {
        var NV = [];
        for (var Oq in jg) {
            var mq = jg[Oq];
            if (jg.hasOwnProperty(Oq)) {
                NV[h1.slice(257, 261)](D_(mq))
            }
        }
        return NV
    }

    function rf(Uh, m7) {
        var AB = [];
        for (var k1 in Uh) {
            var kY = Uh[k1];
            if (Uh.hasOwnProperty(k1)) {
                if (m7(kY)) {
                    AB[h1.slice(257, 261)](kY)
                }
            }
        }
        return AB
    }

    function So(r8, v6) {
        return r8[h1.substr(1350, 9)](r8[uq.substr(1474, 6)] - v6[uq.substr(1474, 6)]) === v6
    }

    function RN(Lk, zL) {
        var by = h1.substring(668, 681);
        if (zL < 2) {
            var fR = h1.substr(936, 18);
            try {
                fR = h1.substr(164, 13) + Lk
            } catch (m2) {
            }
            var fB = Qx.substr(1379, 24);
            try {
                fB = window['JSON'][oF.substr(817, 9)](Lk) + h1.slice(1121, 1121)
            } catch (Bs) {
            }
            var Ha = oF.substr(838, 13);
            try {
                if (typeof Lk[uq.slice(1196, 1200)] === uq.substr(396, 6)) {
                    Ha = Lk[uq.slice(1196, 1200)]
                }
            } catch (TR) {
            }
            var Gi = oF.slice(678, 694);
            try {
                if (typeof Lk[Qx.slice(1131, 1138)] === uq.substr(396, 6)) {
                    Gi = Lk[Qx.slice(1131, 1138)]
                }
            } catch (rB) {
            }
            var Do = h1.slice(205, 219);
            try {
                if (typeof Lk[uq.substring(136, 141)] === uq.substr(396, 6)) {
                    Do = Lk[uq.substring(136, 141)]
                }
            } catch (Mh) {
            }
            var WL = oF.substring(1313, 1327);
            try {
                if (Lk[uq.substring(1553, 1558)]) {
                    WL = RN(Lk[uq.substring(1553, 1558)], zL + 1)
                }
            } catch (nB) {
            }
            by = fR + uq.slice(289, 293) + fB + uq.slice(289, 293) + Ha + uq.slice(289, 293) + Gi + uq.slice(289, 293) + Do + uq.slice(289, 293) + WL
        }
        return by
    }

    function Nl(Zl) {
        var FE = 25928;
        var U9 = {};
        U9[uq.slice(1020, 1021)] = FE;
        U9[Qx.substr(456, 2)] = 0x690da9b3;
        U9[Qx.slice(64, 66)] = 0x7b72ecc5;
        U9[uq.substring(59, 61)] = 2;
        U9[Qx.substring(571, 573)] = "hZgLWCjSTalwQjOd5/Bhn3dQup1ihlZpBOuRP8UergCM9XPJBLHVLw==";
        U9[uq.substring(984, 985)] = RN(Zl, 0);
        return U9
    }

    var gn = new window['RegExp'](uq.substring(402, 404), Qx.substr(886, 1));
    var PB = new window['RegExp'](Qx.substring(1059, 1074), Qx.substr(886, 1));
    var E4 = new window['RegExp'](oF.substring(278, 280), Qx.substr(886, 1));
    var EX = window['JSON'][oF.substr(817, 9)];
    // var r0 = window[oF.substr(573, 6)][Qx.substr(136, 12)];
    var r0 = window['String']['fromCharCode'];
    var eG = window[h1.substring(869, 877)];
    console.log(h1.substring(869, 877))
''')


print(f"拦截到的URL: {result}")
